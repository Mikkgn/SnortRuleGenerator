import re

from pyshark.packet.fields import LayerFieldsContainer

from analyzer.db.models import SearchType, Criterion, Sign
from typing import List, Optional, Iterable, Tuple, Any, Mapping, Dict, Union

from pyshark.packet.packet import Packet
from analyzer.db.models import AttackDefinition, Sign


class AttackSignWrapper:
    def __init__(self, sign: Sign):
        self._sign = sign
        self._detected = False
        self._packet: Optional[Packet] = None
        self._index_of_founded_packet: Optional[int] = None
        self._timestamp: Optional[int] = None

    @property
    def src(self):
        return self._sign.src

    @property
    def dst(self):
        return self._sign.dst

    @property
    def is_detected(self) -> bool:
        return self._detected

    def assign_result(self, packet: Packet, result: Any) -> None:
        if result is True:
            self._detected = result
            self._packet = packet
            self._timestamp = packet.sniff_time
            self._index_of_founded_packet = packet.number

    @property
    def packet_type(self):
        return self._sign.packet_type.name

    @property
    def search_keys(self) -> Iterable[Tuple[str, str]]:
        for key, value in self._sign.checked_fields.items():
            yield key, value

    @property
    def search_type(self):
        return self._sign.search_type

    @property
    def criteria(self):
        return self._sign.result_criteria

    def reset(self):
        self._detected = False
        self._packet = None
        self._timestamp = None
        self._index_of_founded_packet = None


class Attack(object):
    def __init__(self, attack: AttackDefinition):
        self._signs: List[AttackSignWrapper] = [AttackSignWrapper(sign) for sign in attack.signs]
        self._is_detected = False

    @property
    def current_sign(self) -> AttackSignWrapper:
        for sign in self._signs:
            if not sign.is_detected:
                return sign

    def is_attack_detected(self):
        for sign in self._signs:
            if not sign.is_detected:
                return False
        else:
            self._reset()
            return True

    def _reset(self):
        for sign in self._signs:
            sign.reset()


def is_net_include_ip(ipv4_address, netmask):
    return True


def is_value_satisfies_condition(search_value: Union[str, int], search_type: SearchType,
                                 value: Optional[LayerFieldsContainer] = None) -> bool:
    if value is None:
        return False
    datatype = type(search_value)
    if search_type == SearchType.REGEX:
        pattern = re.compile(search_value)
        if len(pattern.findall(value)):
            return True
    if search_type == SearchType.FULL_MATCH:
        return datatype(value) == search_value


def evaluate_result(summary_check_result: List[bool], check_type: Criterion) -> bool:
    true_count = sum(summary_check_result)
    if check_type == Criterion.AT_LEAST_ONE:
        if true_count >= 1:
            return True
        else:
            return False
    if check_type == Criterion.ALL:
        if true_count == len(summary_check_result):
            return True
        else:
            return False


def analyze_packet(sign: AttackSignWrapper, packet: Packet, *args: Any, **kwargs: Any):
    if getattr(packet, 'ip', None) is not None:
        if not is_net_include_ip(packet.ip.src, sign.src) or not is_net_include_ip(packet.ip.dst, sign.dst):
            return False
    if sign.packet_type in packet:
        summary_check_result = []
        for key, value in sign.search_keys:
            search_value = getattr(packet[sign.packet_type], key, None)
            if search_value is not None:
                summary_check_result.append(is_value_satisfies_condition(value, sign.search_type, search_value))
            else:
                return False
        if summary_check_result:
            summary_result = evaluate_result(summary_check_result, sign.criteria)
            if summary_result is True:
                return True
    else:
        return False


def packet_to_str(packet: Packet):
    return f"{packet._packet_string} <{packet.highest_layer}> time:<{packet.sniff_time}>"
