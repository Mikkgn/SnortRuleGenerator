import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import UUIDType

from analyzer.db.data_types import Json

Base = declarative_base()

metadata = Base.metadata


class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4())
    message = Column(Json, nullable=False)
    sent = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
