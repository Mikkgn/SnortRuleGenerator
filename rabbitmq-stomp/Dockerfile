FROM rabbitmq:3.8.1

RUN rabbitmq-plugins enable --offline rabbitmq_web_stomp
RUN rabbitmq-plugins enable rabbitmq_management

EXPOSE 15674
EXPOSE 15671 15672