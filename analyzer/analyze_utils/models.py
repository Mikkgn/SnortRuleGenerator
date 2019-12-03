from datetime import datetime
from enum import Enum
from typing import Dict, TypedDict, List

from pyshark.packet.packet import Packet


class EventMessage(TypedDict, total=False):
    attack_id: str
    attack_definition_id: str
    sign_id: str
    packet: Dict
    previous_packets: List[Dict]
    created_at: datetime
    event_type: str


class AnalyzeResult(Enum):
    DETECTED = 0
    NOT_DETECTED = 1
    PACKET_TYPE_NOT_EQUAL = 2
    IP_NOT_IN_NETWORK = 3
    UNKNOWN = 4


def packet_to_str(packet: Packet) -> str:
    return f"{packet._packet_string} <{packet.highest_layer}> time:<{packet.sniff_time}>"


def packet_to_dict(packet):
    d = dict()
    for layer in packet.layers:
        layer_dict = {}
        for field in layer.field_names:
            layer_dict[field] = str(getattr(layer, field))
        d[layer.layer_name] = layer_dict
    return d
