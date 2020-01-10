# type: ignore
import asyncio
from multiprocessing import Queue
from typing import Mapping, Optional, Dict, Literal, TypedDict, Type, Any, List

import pika
from pika import BasicProperties
from pika import channel
from pika.spec import Basic

from analyzer.analyze_utils import AttackSign
from analyzer.packet_analyzer import PacketAnalyzer
from analyzer.reader import PcapReader, InterfaceReader, PacketReader
from common.amqp_consumer import AMQPClient
from common.amqp_publisher import AMQPPublisher

READERS = Literal['pcap', 'interface']
ACTIONS = Literal['start', 'stop']


class StartOrStopRequest(TypedDict, total=False):
    reader: READERS
    action: ACTIONS
    definitions: List[Dict]
    home_network: str
    external_network: str


class Listener(AMQPClient):
    """
    Thread, that listen RMQ command queue
    """
    LISTENER_EXCHANGE_NAME = 'listener'
    LISTENER_STARTUP_QUEUE_NAME = 'reader_start_or_stop'
    LISTENER_STARTUP_ROUTING_KEY = 'action'

    readers_mapper: Mapping[READERS, Type[PacketReader]] = {
        'pcap': PcapReader,
        'interface': InterfaceReader
    }

    def __init__(self, host: str, user: str, password: str):
        super().__init__(host, user, password)
        self._current_process: Optional[PacketReader] = None
        self._queue = Queue()
        self._publisher = AMQPPublisher(host, user, password)
        self._analyzer: Optional[PacketAnalyzer] = None
        self.add_consumer(self.LISTENER_EXCHANGE_NAME, self.LISTENER_STARTUP_QUEUE_NAME,
                          self.LISTENER_STARTUP_ROUTING_KEY, self._handle_start_or_stop_message)

    def _handle_start_or_stop_message(self, _unused_channel: pika.channel.Channel, basic_deliver: Basic.Deliver,
                                      properties: BasicProperties, data: StartOrStopRequest):
        """
        Handle start or stop message from RMQ
        """
        request = StartOrStopRequest(**data)
        if 'action' not in request:
            self._logger.warning(f"Not specified action in message")
            return
        if 'reader' not in request and request['action'] != 'stop':
            self._logger.warning(f"Not specified reader in message")
            return
        self._process_start_or_stop_event(**request)

    def _process_start_or_stop_event(self, action: ACTIONS,
                                     reader: Optional[READERS] = None,  *args: Any, **kwargs: Any):
        asyncio.set_event_loop(asyncio.new_event_loop())
        if action == 'stop':
            self._stop_reader()
        else:
            self._start_reader(reader, *args, **kwargs)

    def _start_reader(self, reader: READERS, signs: List[Dict], *args: Any, **kwargs: Any):
        if self._current_process is not None:
            self._logger.warning(f"Процесс уже запущен")
            return
        reader_cls = self.readers_mapper[reader]
        self._current_process = reader_cls(queue_=self._queue, *args, **kwargs)
        self._current_process.start()
        signs_ = [AttackSign(**sign) for sign in signs]
        self._analyzer = PacketAnalyzer(queue_=self._queue, signs=signs_, *args, **kwargs)
        self._analyzer.start()
        self._publisher.publish('analyzer', 'status.changed', {'status': 'active'})

    def _stop_reader(self):
        if self._current_process is None:
            self._logger.warning(f"Процесс не запущен")
            return
        self._current_process.stop_read(timeout=10)
        self._current_process = None
        self._analyzer.stop_analyze()
        self._analyzer = None
        self._publisher.publish('analyzer', 'status.changed', {'status': 'disabled'})
