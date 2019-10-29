import logging

import queue
import time
from concurrent.futures import ProcessPoolExecutor, as_completed, Future
from multiprocessing import Process, Event as ProcEvent, Queue
from typing import List, Tuple, Dict

from pyshark.packet.packet import Packet

from analyzer.config import configuration
from analyzer.db.engine import create_scoped_session
from analyzer.db.models import Definition
from analyzer.utils import analyze_packet, DefinitionWrapper, packet_to_str


class PacketAnalyzer(Process):
    def __init__(self, queue_: Queue):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._queue = queue_
        self._scoped_session = create_scoped_session(configuration["db_config"])
        self._definitions: List[DefinitionWrapper] = []
        self._stop_event = ProcEvent()
        self._load_definitions()
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

    def _load_definitions(self):
        try:
            self._scoped_session.commit()
            definitions: List[Definition] = self._scoped_session.query(Definition).all()
        except Exception as exc:
            self._logger.exception(exc)
        else:
            self._definitions = [DefinitionWrapper(attack_definition) for attack_definition in definitions]

    def analyze_packet(self, packet: Packet) -> None:
        future_to_sign_map: Dict[Future, Tuple[DefinitionWrapper, Packet]] = {}
        worker_list = []
        with ProcessPoolExecutor(max_workers=1) as worker:
            for definition in self._definitions:
                fut = worker.submit(analyze_packet, definition.current_sign, packet)
                future_to_sign_map[fut] = (definition, packet)
                worker_list.append(fut)
            for future in as_completed(worker_list):
                definition, packet = future_to_sign_map[future]
                self._logger.debug(f"Analyzed {packet_to_str(packet)}")
                definition.current_sign.assign_result(packet, future.result(), self._scoped_session)
                if definition.is_attack_detected():
                    self._logger.warning(f"Attack detected")

    def stop(self):
        self._stop_event.set()

