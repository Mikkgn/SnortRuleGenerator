import logging
from typing import TypedDict, Dict

import pika
from pika import BasicProperties
from pika import channel
from pika.spec import Basic

from api.db.models import Rule
from common.amqp_consumer import AMQPClient


class RuleMessage(TypedDict, total=False):
    rule: str


class RuleHandler(AMQPClient):
    """
    Thread, that listen RMQ queues
    """

    def __init__(self, host: str, user: str, password: str, scoped_session):
        super().__init__(host, user, password)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._scoped_session = scoped_session
        self.add_consumer('rules', 'add_rules_to_db', 'rule.created', self._handle_rule_message)

    def _handle_rule_message(self, _unused_channel: pika.channel.Channel, basic_deliver: Basic.Deliver,
                             properties: BasicProperties, data: RuleMessage):
        """
        Handle start or stop message from RMQ
        """
        message = RuleMessage(**data)
        self._add_rule_to_db(message)

    def _add_rule_to_db(self, message: Dict):
        try:
            self._scoped_session.add(Rule(**message))
            self._scoped_session.commit()
        except Exception as exc:
            self._logger.exception(exc)
        finally:
            self._scoped_session.remove()
