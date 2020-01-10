import logging
import typing as t
from string import Template

import pika
from pika import BasicProperties
from pika import channel
from pika.spec import Basic

from common.amqp_consumer import AMQPClient
from common.amqp_publisher import AMQPPublisher


class Packet(t.TypedDict, total=False):
    ip: t.Dict[str, t.Dict]
    tcp: t.Dict[str, t.Dict]
    http: t.Optional[t.Dict[str, t.Dict]]


class EventMessage(t.TypedDict, total=False):
    packet: Packet
    sign: t.Dict


class RuleCreator(AMQPClient):
    rule_template = 'alert tcp $source_ip any -> $destination_ip $destination_port ($content)'

    def __init__(self, rabbitmq_config: t.Dict, exchange_config: t.Dict):
        super().__init__(**rabbitmq_config)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._publisher = AMQPPublisher(**rabbitmq_config)
        self.add_consumer(**exchange_config, callback=self._generate_rule)
        self._sid_count = 10000000

    def _generate_rule(self, _unused_channel: pika.channel.Channel, basic_deliver: Basic.Deliver,
                       properties: BasicProperties, data: EventMessage):
        self._sid_count += 1
        source_ip, destination_ip = self._get_src_and_destination(data['sign'])
        content = self._generate_content(data['packet'], data['sign'])
        dst_port = data['packet']['tcp']['dstport']
        rule = Template(self.rule_template).substitute(source_ip=source_ip, destination_ip=destination_ip,
                                                       destination_port=dst_port, content=content)
        self._publisher.publish('rules', 'rule.created', dict(body=rule))

    def _generate_content(self, packet: t.Dict, sign: t.Dict) -> str:
        regex_patterns = []
        contents = ['content: "{}"'.format(packet['http']['request_uri_path'])]
        for checked_field in sign['checked_fields']:
            search_type = checked_field.pop('search_type')
            if search_type == 'REGEX':
                _, value = checked_field.popitem()
                regex_patterns.append(value)
            if search_type == 'FULL_MATCH':
                _, value = checked_field.popitem()
                contents.append(f'content: "{value}";')
        pcre_string = '|'.join(regex_patterns)
        content = f'{" ".join(contents)}; pcre:"{pcre_string}"; sid: {str(self._sid_count)}'
        return content

    def _get_src_and_destination(self, sign: t.Dict) -> t.Tuple[str, str]:
        source_ip = f"${sign['src']}"
        desination_ip = f"${sign['dst']}"
        return source_ip, desination_ip
