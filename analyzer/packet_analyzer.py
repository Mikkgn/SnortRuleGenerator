import logging

import queue
import time
from concurrent.futures import ProcessPoolExecutor, as_completed, Future
from multiprocessing import Process, Event as ProcEvent, Queue
from typing import List, Tuple, Dict

from pyshark.packet.packet import Packet

from analyzer.db.engine import create_scoped_session
from analyzer.db.models import AttackDefinition
from analyzer.utils import analyze_packet, Attack, packet_to_str


class PacketAnalyzer(Process):
    def __init__(self, queue_: Queue):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._queue = queue_
        self._scoped_session = create_scoped_session()
        self._definitions = []
        self._attacks: List[Attack] = []
        self._stop_event = ProcEvent()
        self._load_definitions()
        super().__init__()

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
            attack_definitions: List[AttackDefinition] = self._scoped_session.query(AttackDefinition).all()
        except Exception as exc:
            self._logger.exception(exc)
        else:
            self._attacks = [Attack(attack_definition) for attack_definition in attack_definitions]

    def analyze_packet(self, packet: Packet):
        future_to_sign_map: Dict[Future, Tuple[Attack, Packet]] = {}
        worker_list = []
        with ProcessPoolExecutor(max_workers=4) as worker:
            for attack in self._attacks:
                fut = worker.submit(analyze_packet, attack.current_sign, packet)
                future_to_sign_map[fut] = (attack, packet)
                worker_list.append(fut)
            for future in as_completed(worker_list):
                attack, packet = future_to_sign_map[future]
                self._logger.debug(f"Analyzed {packet_to_str(packet)}")
                attack.current_sign.assign_result(packet, future.result())
                if attack.is_attack_detected():
                    self._logger.warning(f"Attack detected")

    def stop(self):
        self._stop_event.set()

