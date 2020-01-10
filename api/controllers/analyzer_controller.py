from typing import Dict

from connexion import NoContent
from flask import current_app

from common.amqp_publisher import AMQPPublisher


def start_traffic_analyzer(start_request: Dict):  # noqa: E501
    """Start traffic analyzer
    :rtype: int
    """
    publisher: AMQPPublisher = current_app.amqp_publisher
    publisher.publish('listener', 'action', start_request)
    return NoContent, 204


def stop_traffic_analyzer():  # noqa: E501
    """Start traffic analyzer

     # noqa: E501


    :rtype: None
    """
    publisher: AMQPPublisher = current_app.amqp_publisher
    publisher.publish('listener', 'action', {'action': 'stop'})
    return 204
