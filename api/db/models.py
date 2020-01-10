import uuid
from datetime import datetime
from enum import Enum

from common.db.data_types import Json
from sqlalchemy import Column, Enum as EnumField, ForeignKey, DateTime, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from common.db.orm import Base

metadata = Base.metadata


class NetType(Enum):
    EXTERNAL = 0
    HOME = 1


class Criterion(Enum):
    ALL = 0
    AT_LEAST_ONE = 1


class PacketType(Enum):
    IP = 0
    TCP = 1
    HTTP = 2
    ANY = 3

    @classmethod
    def tostring(cls) -> str:
        return cls.name


class Sign(Base):
    __tablename__ = 'signs'

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    packet_type = Column(EnumField(PacketType), nullable=False)
    src = Column(EnumField(NetType), default=NetType.EXTERNAL, nullable=False)
    dst = Column(EnumField(NetType), default=NetType.HOME, nullable=False)
    checked_fields = Column(Json)
    result_criteria = Column(EnumField(Criterion), default=Criterion.AT_LEAST_ONE, nullable=False)


class Event(Base):
    __tablename__ = 'attack_events'

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4)
    sign_id = Column(UUIDType, ForeignKey('signs.id', ondelete='CASCADE'), nullable=True, index=True)
    sign = relationship('Sign')
    packet = Column(Json, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)


class Rule(Base):
    __tablename__ = 'rules'

    number = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(String, nullable=False)


class AnalyzerEnumStatus(Enum):
    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'

    @classmethod
    def fromstr(cls, value: str) -> 'AnalyzerEnumStatus':
        return cls[value.upper()]


class AnalyzerStatus(Base):
    __tablename__ = 'analyzer_status'
    status = Column(EnumField(AnalyzerEnumStatus), nullable=False, default=AnalyzerEnumStatus.DISABLED,
                    primary_key=True)
