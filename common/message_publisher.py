import logging
import uuid
from datetime import datetime
from threading import Thread, Event

import time
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy_utils import UUIDType

from common.amqp_publisher import AMQPPublisher
from common.db.data_types import Json
from common.db.orm import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUIDType, primary_key=True, nullable=False, default=uuid.uuid4)
    data = Column(Json, nullable=False)
    routing_key = Column(String, nullable=False)
    sent = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)


class MessagePublisher(Thread):
    def __init__(self, host: str, user: str, password: str, scoped_session, exchange_name: str):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._stopping = Event()
        self._exchange = exchange_name
        self._scoped_session = scoped_session
        self._amqp_publisher = AMQPPublisher(host, user, password)

    def publish_message(self):
        try:
            message: Message = self._scoped_session.query(Message).filter(Message.sent.is_(False)) \
                .order_by(Message.created_at.asc()).first()
            if message is None:
                return
            self._amqp_publisher.publish(self._exchange, message.routing_key, message.data)
            # self._stomp_connection.send('/queue/events', body=json.dumps(message.message, ensure_ascii=False))
            message.sent = True
            self._scoped_session.commit()
        except Exception as exc:
            self._logger.exception(exc)
        finally:
            self._scoped_session.remove()

    def run(self):
        self._logger.info(f"Запуск {self.__class__.__name__}")
        while not self._stopping.is_set():
            try:
                self.publish_message()
            except Exception as exc:
                self._logger.exception(exc)
            finally:
                time.sleep(3)

    def stop(self):
        self._logger.info(f"Остановка {self.__class__.__name__}")
        self._stopping.set()
        self.join(5)
