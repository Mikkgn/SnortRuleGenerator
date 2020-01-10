import json
import logging
import typing as t

import pika


class AMQPPublisherError(Exception):
    pass


class AMQPPublisher(object):
    def __init__(self, host: str, user: str, password: str):
        self._connection = None
        self._channel: t.Optional[pika.adapters.blocking_connection.BlockingChannel] = None
        self._logger = logging.getLogger(self.__class__.__name__)
        self._connection_params = pika.ConnectionParameters(host=host, port=5672, connection_attempts=20,
                                                            credentials=pika.PlainCredentials(username=user,
                                                                                              password=password))

    def publish(self, exchange, routing_key, data: t.Dict):
        try:
            try:
                self._publish(exchange, routing_key, data)
            except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed):
                self._connection.close(), self._channel.close()
                self._publish(exchange, routing_key, data)
        except pika.exceptions.AMQPConnectionError as e:
            raise AMQPPublisherError(f"Ошибка соединения с Broker: {e.__class__.__name__}: {e.__repr__()}")
        except pika.exceptions.AMQPChannelError as e:
            raise AMQPPublisherError(f"Ошибка создания канала: {e.__class__.__name__}: {e.__repr__()}")
        except Exception as e:
            raise AMQPPublisherError(f"Неизвестная ошибка при отправке сообщения: {e}")

    def _publish(self, exchange, routing_key, data: t.Dict, type='topic'):
        if not self._connection or not self._connection.is_open:
            self._connection = pika.BlockingConnection(self._connection_params)

        if not self._channel or not self._channel.is_open:
            self._channel = self._connection.channel()
        if exchange:
            self._channel.exchange_declare(exchange=exchange, exchange_type=type, durable=True)
        self._channel.basic_publish(exchange, routing_key, json.dumps(data))

        self._logger.info(f"Сообщение '{routing_key}' успешно отправлено в '{exchange}'")
