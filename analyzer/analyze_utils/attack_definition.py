import uuid
from typing import Dict, List, Any

from pyshark.packet.packet import Packet

from analyzer.analyze_utils.attack_sign import AttackSign
from analyzer.analyze_utils.models import AnalyzeResult


class AttackDefinition(object):
    def __init__(self, definition: Dict):
        self._signs: List[AttackSign] = [AttackSign(definition_id=definition['id'], **sign)
                                         for sign in definition['signs']]
        self._is_detected = False
        self.attack_unique_id = uuid.uuid4()
        self._definition = definition
        self.reset_founded_signs()

    def __getitem__(self, item):
        return self._definition[item]

    @property
    def current_sign(self) -> AttackSign:
        for sign in self._signs:
            if not sign.is_detected:
                return sign
        raise RuntimeError(f"Не указаны сигнатуры для определения {self['name']}")

    def is_attack_detected(self):
        for sign in self._signs:
            if not sign.is_detected:
                return False
        else:
            self.reset_founded_signs()
            return True

    def process_packet(self, packet: Packet, *args: Any, **kwargs: Any) -> AnalyzeResult:
        for sign in self._signs:
            if not sign.is_detected:
                return sign.analyze_packet(packet, *args, **kwargs)
        else:
            raise RuntimeError()

    def reset_founded_signs(self):
        self.attack_unique_id = uuid.uuid4()
        for sign in self._signs:
            sign.reset(self.attack_unique_id)
