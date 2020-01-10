import logging
import queue
from concurrent.futures import ProcessPoolExecutor, as_completed, Future, ThreadPoolExecutor
from multiprocessing import Process, Event as ProcEvent, Queue
from typing import List, Tuple, Dict

import time
from pyshark.packet.packet import Packet

from analyzer.analyze_utils.attack_sign import AttackSign
from analyzer.analyze_utils.models import EventMessage, packet_to_dict, packet_to_str, AnalyzeResult
from analyzer.config import configuration
from common.amqp_publisher import AMQPPublisher


class PacketAnalyzer(Process):
    def __init__(self, queue_: Queue, signs: List[AttackSign], home_network: str, external_network: str,
                 *args, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._queue = queue_
        self._home_network = home_network
        self._publisher = AMQPPublisher(**configuration['rabbitmq_config'])
        self._external_network = external_network
        self._signs: List[AttackSign] = signs
        self._stop_event = ProcEvent()
        self._cache_limit = configuration['cache_limit']

        super().__init__(name=self.__class__.__name__)

    def run(self):
        self._logger.info(f"Starting {self.__class__.__name__}")
        while not self._stop_event.is_set():
            try:
                packet = self._queue.get_nowait()
            except queue.Empty:
                time.sleep(1)
            except Exception as exc:
                self._logger.exception(exc)
            else:
                self._logger.info(f"Captured {packet_to_str(packet)}")
                self.analyze_packet(packet)

    def stop_analyze(self, timeout: int = 10):
        self.stop()
        self.join(timeout)
        self.terminate()

    def analyze_packet(self, packet: Packet) -> None:
        """
        """
        future_to_sign_map: Dict[Future, Tuple[AttackSign, Packet]] = {}
        worker_list = []
        with ThreadPoolExecutor(max_workers=1) as worker:
            for sign in self._signs:
                fut = worker.submit(sign.analyze_packet, packet,
                                    self._home_network, self._external_network)
                future_to_sign_map[fut] = (sign, packet)
                worker_list.append(fut)
            for future in as_completed(worker_list):
                sign, packet = future_to_sign_map[future]
                result = future.result()
                if result == AnalyzeResult.DETECTED:
                    self._logger.warning(f"Sign {sign.name}")
                    self._send_event(packet, sign)

    def _send_event(self, packet: Packet, sign: AttackSign):
        """
        Function add Event Message to RabbitMQ queue
        """
        event_message = EventMessage(sign_id=sign['id'], packet=packet_to_dict(packet), sign=sign.to_dict())
        self._publisher.publish('attack_event', 'attack.detected', event_message)

    def stop(self):
        self._logger.info(f"Stopping {self.__class__.__name__}")
        self._stop_event.set()
