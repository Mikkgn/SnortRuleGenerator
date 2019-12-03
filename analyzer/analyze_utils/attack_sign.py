import logging
import re
import uuid
from typing import TypedDict, Dict, Optional, Any, Union, List

from pyshark.packet.fields import LayerFieldsContainer
from pyshark.packet.packet import Packet

from analyzer.analyze_utils.models import AnalyzeResult
from common.enum_types import SearchType, Criterion

logger = logging.getLogger(__name__)

class SignInterface(TypedDict, total=False):
    src: str
    dst: str
    id: str
    packet_type: str
    search_type: str
    checked_fields: Dict
    result_criteria: str
    order: int


class AttackSign:
    def __init__(self, definition_id: str, **kwargs: Any):
        self._definition_id = definition_id
        self._sign: SignInterface = {}
        self.attack_unique_id: Optional[uuid.UUID] = None
        self._detected = False
        self._packet: Optional[Packet] = None
        self._timestamp: Optional[int] = None
        for key, value in kwargs.items():
            self._sign[key] = value

    def __getitem__(self, key: str):
        return self._sign[key]

    @property
    def is_detected(self) -> bool:
        return self._detected

    @property
    def search_type(self) -> SearchType:
        return SearchType.fromstring(self['search_type'])

    @property
    def criterion(self) -> Criterion:
        return Criterion.fromstring(self['result_criteria'])

    def mark_as_detected(self, packet: Packet) -> None:
        """
        Mark sign as detected and assign packet
        :param packet:
        :return:
        """
        self._detected = True
        self._packet = packet
        self._timestamp = packet.sniff_time

    def reset(self, attack_id: uuid.UUID) -> None:
        """
        Reset
        :param attack_id:
        :return:
        """
        self.attack_unique_id = attack_id
        self._detected = False
        self._packet = None
        self._timestamp = None

    def analyze_packet(self, packet: Packet, home_net: str, external_net: str,
                       *args: Any, **kwargs: Any) -> AnalyzeResult:
        """
        Analyze packet to equality attack sign. If packet equal, add event to database
        :param packet: Packet
        :param home_net: str
        :param external_net: str
        :param args:
        :param kwargs:
        :return:
        """
        if self['packet_type'] in packet:
            if not self.is_net_includes(packet, home_net, external_net):
                return AnalyzeResult.IP_NOT_IN_NETWORK
            result = self._check_fields(packet)
            if result is True:
                return AnalyzeResult.DETECTED
            return AnalyzeResult.NOT_DETECTED
        else:
            return AnalyzeResult.PACKET_TYPE_NOT_EQUAL

    def _check_fields(self, packet: Packet):
        """
        Check packet fields to equality sign fields
        :param packet:
        :return:
        """
        summary_check_result = []

        logger.info(self._sign)
        for key, value in self['checked_fields'].items():
            search_value = getattr(packet[self['packet_type']], key, None)
            if search_value is not None:
                summary_check_result.append(self._is_value_satisfies_condition(value, search_value))
            else:
                return False
        if summary_check_result:
            return self._evaluate_result(summary_check_result)
        else:
            return False

    def _is_value_satisfies_condition(self, search_value: Union[str, int],
                                      value: Optional[LayerFieldsContainer] = None) -> bool:
        """
        Check packet field value to equality sign field
        :param search_value:
        :param value:
        :return:
        """
        if value is None:
            return False
        datatype = type(search_value)
        if self.search_type == SearchType.REGEX and isinstance(search_value, str):
            pattern = re.compile(search_value)
            if len(pattern.findall(value)):
                return True
        if self.search_type == SearchType.FULL_MATCH:
            return datatype(value) == search_value
        else:
            raise ValueError(f"Указан неизвестный тип сравнения {self.search_type.name}")

    def is_net_includes(self, packet: Packet, home_net: str, external_net: str):
        """
        Check, that packet source and destination ip includes home or external network
        :param packet:
        :param home_net:
        :param external_net:
        :return:
        """
        if getattr(packet, 'ip', None) is not None:
            if is_net_include_ip(packet.ip.src, self['src'], home_net, external_net) \
                    and is_net_include_ip(packet.ip.dst, self['dst'], home_net, external_net):
                return True

        return False

    def _evaluate_result(self, check_result: List[bool]) -> bool:
        true_count = sum(check_result)
        if self.criterion == Criterion.AT_LEAST_ONE:
            if true_count >= 1:
                return True
            else:
                return False
        elif self.criterion == Criterion.ALL:
            if true_count == len(check_result):
                return True
            else:
                return False
        else:
            raise ValueError(f"Указан неизвестный тип {self.criterion}")


def is_net_include_ip(ipv4_address, netmask, home_net, external_net):
    return True
