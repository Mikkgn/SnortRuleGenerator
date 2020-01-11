import logging
from typing import TypedDict, Dict

import pika
from pika import BasicProperties
from pika import channel
from pika.spec import Basic

from api.db.models import Event
from common.amqp_consumer import AMQPClient


class EventMessage(TypedDict, total=False):
    sign_id: str
    packet: dict


class EventsHandler(AMQPClient):
    """
    Thread, that listen RMQ queues
    """

    def __init__(self, host: str, user: str, password: str, scoped_session):
        super().__init__(host, user, password)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._scoped_session = scoped_session
        self.add_consumer('attack_event', 'add_event_to_db', 'attack.detected', self._handle_event_message)

    def _handle_event_message(self, _unused_channel: pika.channel.Channel, basic_deliver: Basic.Deliver,
                              properties: BasicProperties, data: EventMessage):
        """
        Handle start or stop message from RMQ
        """
        message = EventMessage(**data)
        self._update_analyzer_status(message)

    def _update_analyzer_status(self, message: Dict):
        try:
            self._scoped_session.add(Event(sign_id=message['sign_id'], packet=message['packet']))
            self._scoped_session.commit()
        except Exception as exc:
            self._logger.exception(exc)
        finally:
            self._scoped_session.remove()
