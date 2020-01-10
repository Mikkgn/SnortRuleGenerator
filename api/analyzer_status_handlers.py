import logging
from typing import Literal, TypedDict, Union

import pika
from pika import BasicProperties
from pika import channel
from pika.spec import Basic

from api.db.models import AnalyzerStatus, AnalyzerEnumStatus
from common.amqp_consumer import AMQPClient


class AnalyzerStatusMessage(TypedDict, total=False):
    status: Union[Literal["active"], Literal["disabled"]]


class AnalyzerStatusHandler(AMQPClient):
    """
    Thread, that listen RMQ queues
    """

    def __init__(self, host: str, user: str, password: str, scoped_session):
        super().__init__(host, user, password)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._scoped_session = scoped_session
        self.add_consumer('analyzer', 'update_status_in_db', 'status.changed', self._handle_analyzer_status_message)

    def _handle_analyzer_status_message(self, _unused_channel: pika.channel.Channel, basic_deliver: Basic.Deliver,
                                        properties: BasicProperties, data: AnalyzerStatusMessage):
        """
        Handle start or stop message from RMQ
        """
        message = AnalyzerStatusMessage(**data)
        self._update_analyzer_status(**message)

    def _update_analyzer_status(self, status: str):
        try:
            analyzer: AnalyzerStatus = self._scoped_session.query(AnalyzerStatus).one()
            analyzer.status = AnalyzerEnumStatus.fromstr(status)
            self._scoped_session.commit()
        except Exception as exc:
            self._logger.exception(exc)
        finally:
            self._scoped_session.remove()
