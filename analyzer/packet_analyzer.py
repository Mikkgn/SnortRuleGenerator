import logging
import queue
import time
import uuid
from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed, Future
from multiprocessing import Process, Event as ProcEvent, Queue
from typing import List, Tuple, Dict, Deque, Optional


from pyshark.packet.packet import Packet

from analyzer.analyze_utils.attack_definition import AttackDefinition
from analyzer.analyze_utils.attack_sign import AttackSign
from analyzer.analyze_utils.models import EventMessage, packet_to_dict, packet_to_str
from analyzer.config import configuration
from analyzer.db.models import Message
from common.db.engine import create_scoped_session
from common.enum_types import EventType


class PacketAnalyzer(Process):
    def __init__(self, queue_: Queue, definitions: List[AttackDefinition], home_network: str, external_network: str,
                 *args, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._queue = queue_
        self._scoped_session = create_scoped_session(configuration["db_config"])
        self._home_network = home_network
        self._external_network = external_network
        self._definitions: List[DefinitionWrapper] = definitions
        self._stop_event = ProcEvent()
        self._packets_cache: Deque[Packet] = deque([])
        self._cache_limit = configuration['cache_limit']

        super().__init__(name=self.__class__.__name__)

    def run(self):
        while not self._stop_event.is_set():
            try:
                packet = self._queue.get_nowait()
            except queue.Empty:
                time.sleep(1)
            except Exception as exc:
                self._logger.exception(exc)
            else:
                self.analyze_packet(packet)
                self._add_to_cache(packet)

    def stop_analyze(self, timeout: int = 10):
        self.stop()
        self.join(timeout)
        self.terminate()

    def _add_to_cache(self, packet: Packet) -> None:
        self._packets_cache.append(packet)
        if len(self._packets_cache) > self._cache_limit:
            self._packets_cache.popleft()

    def analyze_packet(self, packet: Packet) -> None:
        future_to_sign_map: Dict[Future, Tuple[AttackDefinition, Packet]] = {}
        worker_list = []
        with ProcessPoolExecutor(max_workers=4) as worker:
            for definition in self._definitions:
                fut = worker.submit(definition.process_packet, definition.current_sign, packet,
                                    self._home_network, self._external_network)
                future_to_sign_map[fut] = (definition, packet)
                worker_list.append(fut)
            for future in as_completed(worker_list):
                definition, packet = future_to_sign_map[future]
                self._logger.debug(f"Analyzed {packet_to_str(packet)}")
                result = future.result()
                if result is True:
                    self._send_event(EventType.SIGN_DETECTED, packet, sign=definition.current_sign)
                if definition.is_attack_detected():
                    self._logger.warning(f"Attack detected")
                    self._send_event(EventType.ATTACK_DETECTED, packet, definition=definition)

    def _send_event(self, event_type: EventType, packet: Packet, sign: Optional[AttackSign] = None,
                    definition: Optional[AttackDefinition] = None):
        if sign is not None:
            event_message = EventMessage(sign_id=sign['id'], packet=packet_to_dict(packet),
                                         attack_id=sign.attack_unique_id, previous_packets=self._packets_cache,
                                         event_type=event_type.tostring())
        elif definition is not None:
            event_message = EventMessage(attack_id=definition.attack_unique_id,
                                         event_type=event_type.tostring(), attack_definition_id=definition['id'])
        else:
            return
        message = Message(id=uuid.uuid4(), message=event_message)
        self._scoped_session.add(message)
        self._scoped_session.commit()

    def stop(self):
        self._stop_event.set()
