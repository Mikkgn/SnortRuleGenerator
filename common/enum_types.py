from enum import Enum


class SearchType(Enum):
    REGEX = 0
    FULL_MATCH = 1

    @classmethod
    def fromstring(cls, value: str) -> 'SearchType':
        return cls[value.upper()]


class NetType(Enum):
    EXTERNAL = 0
    HOME = 1


class Criterion(Enum):
    ALL = 0
    AT_LEAST_ONE = 1

    @classmethod
    def fromstring(cls, value: str) -> 'Criterion':
        return cls[value.upper()]


class PacketType(Enum):
    IP = 0
    TCP = 1
    HTTP = 2
    ANY = 3

    def tostring(cls) -> str:
        return cls.name

    @classmethod
    def fromstring(cls, value: str) -> 'PacketType':
        return cls[value.upper()]


class EventType(Enum):
    SIGN_DETECTED = 0
    ATTACK_DETECTED = 1

    def tostring(self) -> str:
        return self.name

    @classmethod
    def fromstring(cls, value: str) -> 'EventType':
        return cls[value.upper()]
