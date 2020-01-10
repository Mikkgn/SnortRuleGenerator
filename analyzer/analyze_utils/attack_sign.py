import logging
import re
from copy import deepcopy
from typing import TypedDict, Dict, Optional, Any, Union, List, Literal

from pyshark.packet.fields import LayerFieldsContainer
from pyshark.packet.packet import Packet

from analyzer.analyze_utils.models import AnalyzeResult
from common.enum_types import SearchType, Criterion

logger = logging.getLogger(__name__)


class SignInterface(TypedDict, total=False):
    src: str
    dst: str
    id: str
    name: str
    packet_type: str
    checked_fields: Dict
    result_criteria: str


SignInterfaceKeys = Literal['src', 'dst', 'id', 'name', 'packet_type', 'checked_fields', 'result_criteria']


class AttackSign:
    def __init__(self, **kwargs: Dict[str, Any]):
        self._sign: SignInterface = {}
        for key, value in kwargs.items():
            self._sign[key] = value

    def __getitem__(self, key: SignInterfaceKeys):
        return self._sign[key]

    def to_dict(self) -> Dict:
        return self._sign

    @property
    def name(self) -> str:
        return self._sign['name']

    @property
    def _criterion(self) -> Criterion:
        return Criterion.fromstring(self['result_criteria'])

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
        for field in self['checked_fields']:
            checked_field = deepcopy(field)
            search_type = SearchType.fromstring(checked_field.pop('search_type'))
            for key, value in checked_field.items():
                search_value = getattr(packet[self['packet_type']], key, None)
                if search_value is not None:
                    summary_check_result.append(self._is_value_satisfies_condition(value, search_type, search_value))
                else:
                    return False
        if summary_check_result:
            return self._evaluate_result(summary_check_result)
        else:
            return False

    def _is_value_satisfies_condition(self, search_value: Union[str, int], search_type: SearchType,
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
        if search_type == SearchType.REGEX:
            if not isinstance(search_value, str):
                raise ValueError(f"Значение не является строкой")
            pattern = re.compile(search_value)
            if len(pattern.findall(value)):
                return True
            else:
                return False
        elif search_type == SearchType.FULL_MATCH:
            return datatype(value) == search_value
        else:
            raise ValueError(f"Указан неизвестный тип сравнения {search_type.name}")

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
        if self._criterion == Criterion.AT_LEAST_ONE:
            if true_count >= 1:
                return True
            else:
                return False
        elif self._criterion == Criterion.ALL:
            if true_count == len(check_result):
                return True
            else:
                return False
        else:
            raise ValueError(f"Указан неизвестный тип {self._criterion}")


def is_net_include_ip(ipv4_address, netmask, home_net, external_net):
    return True
