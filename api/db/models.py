import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, String, Enum as EnumField, ForeignKey, INTEGER, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from analyzer.db.data_types import Json
from common.enum_types import EventType

INT32_MAX = 2147483647

Base = declarative_base()

metadata = Base.metadata


class SearchType(Enum):
    REGEX = 0
    FULL_MATCH = 1


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


sign_to_definition_table = Table(
    'signs_to_definitions', metadata,
    Column('sign_id', UUIDType, ForeignKey('signs.id', ondelete='CASCADE'), primary_key=True, nullable=False,
           index=True),
    Column('definition_id', UUIDType, ForeignKey('definitions.id', ondelete='CASCADE'), primary_key=True,
           nullable=False,
           index=True)
)


class Sign(Base):
    __tablename__ = 'signs'

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4())
    packet_type = Column(EnumField(PacketType), nullable=False)
    search_type = Column(EnumField(SearchType), default=SearchType.REGEX, nullable=False)
    src = Column(EnumField(NetType), default=NetType.EXTERNAL, nullable=False)
    dst = Column(EnumField(NetType), default=NetType.HOME, nullable=False)
    checked_fields = Column(Json)
    result_criteria = Column(EnumField(Criterion), default=Criterion.AT_LEAST_ONE, nullable=False)
    order = Column(INTEGER, default=0, nullable=False)


class Definition(Base):
    __tablename__ = 'definitions'

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4())
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    signs = relationship('Sign', secondary='signs_to_definitions')
    criterion = Column(EnumField(Criterion), nullable=False, default=Criterion.ALL)


class Event(Base):
    __tablename__ = 'attack_events'

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4())
    attack_id = Column(UUIDType, nullable=False, index=True)
    attack_definition_id = Column(UUIDType, ForeignKey('definitions.id', ondelete='CASCADE'), nullable=True,
                                  index=True)
    attack_definition = relationship('Definition')
    sign_id = Column(UUIDType, ForeignKey('signs.id', ondelete='CASCADE'), nullable=True, index=True)
    sign = relationship('Sign')
    packet = Column(Json, nullable=False)
    event_type = Column(EnumField(EventType), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
