import re
import uuid
import json
import logging
from typing import List, Optional, Iterable, Tuple, Any, Dict, Union

from pyshark.packet.common import Pickleable
from pyshark.packet.fields import LayerFieldsContainer
from pyshark.packet.packet import Packet
from sqlalchemy.orm import Session

from analyzer.db.models import Definition, Sign, EventType
from analyzer.db.models import SearchType, Criterion, Event


class SignWrapper:
    def __init__(self, sign: Sign, definition_id: uuid.UUID):
        self._sign = sign
        self._definition_id = definition_id
        self._attack_unique_id: Optional[uuid.UUID] = None
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

    def assign_result(self, packet: Packet, result: Any, scoped_session: Session) -> None:
        if result is True:
            self._detected = result
            self._packet = packet
            self._timestamp = packet.sniff_time
            self._index_of_founded_packet = packet.number
            event = Event(sign_id=self._sign.id, packet=packet_to_dict(packet), attack_id=self._attack_unique_id,
                          event_type=EventType.SIGN_DETECTED)
            scoped_session.add(event)
            scoped_session.commit()

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

    def reset(self, attack_id: uuid.UUID) -> None:
        self._attack_unique_id = attack_id
        self._detected = False
        self._packet = None
        self._timestamp = None
        self._index_of_founded_packet = None


class DefinitionWrapper(object):
    def __init__(self, definition: Definition):
        self._signs: List[SignWrapper] = [SignWrapper(sign, definition_id=definition.id)
                                          for sign in definition.signs]
        self._is_detected = False
        self._attack_unique_id = uuid.uuid4()
        self._definition = definition
        self._reset()

    @property
    def current_sign(self) -> SignWrapper:
        for sign in self._signs:
            if not sign.is_detected:
                return sign
        raise RuntimeError(f"Не указаны сигнатуры для определения {self._definition.name}")

    def is_attack_detected(self):
        for sign in self._signs:
            if not sign.is_detected:
                return False
        else:
            self._reset()
            return True

    def _reset(self):
        self._attack_unique_id = uuid.uuid4()
        for sign in self._signs:
            sign.reset(self._attack_unique_id)


def is_net_include_ip(ipv4_address, netmask):
    return True


def is_value_satisfies_condition(search_value: Union[str, int], search_type: SearchType,
                                 value: Optional[LayerFieldsContainer] = None) -> bool:
    if value is None:
        return False
    datatype = type(search_value)
    if search_type == SearchType.REGEX and isinstance(search_value, str):
        pattern = re.compile(search_value)
        if len(pattern.findall(value)):
            return True
    if search_type == SearchType.FULL_MATCH:
        return datatype(value) == search_value
    else:
        raise ValueError(f"Указан неизвестный тип сравнения {search_type.name}")


def evaluate_result(summary_check_result: List[bool], check_type: Criterion) -> bool:
    true_count = sum(summary_check_result)
    if check_type == Criterion.AT_LEAST_ONE:
        if true_count >= 1:
            return True
        else:
            return False
    elif check_type == Criterion.ALL:
        if true_count == len(summary_check_result):
            return True
        else:
            return False
    else:
        raise ValueError(f"Указан неизвестный тип {check_type}")


def analyze_packet(sign: SignWrapper, packet: Packet, *args: Any, **kwargs: Any) -> bool:
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
            return evaluate_result(summary_check_result, sign.criteria)
        else:
            return False
    else:
        return False


def packet_to_str(packet: Packet) -> str:
    return f"{packet._packet_string} <{packet.highest_layer}> time:<{packet.sniff_time}>"


def packet_to_dict(packet: Packet) -> Dict:
    def obj_to_dict(value):
        if isinstance(value, Pickleable):
            d = value.__dict__
            for key, value in d.items():
                d[key] = obj_to_dict(value)
        else:
            d = value
        return d

    return obj_to_dict(packet)

