from analyzer.config import configuration
from analyzer.listener import Listener
from common.amqp_publisher import AMQPPublisher
from common.db.engine import wait_db, init_db, create_scoped_session


def main():
    wait_db(**configuration["db_config"])
    init_db(configuration["db_config"])
    # import sys
    # sys.path.append('./pydevd-pycharm.egg')
    # import pydevd_pycharm
    # pydevd_pycharm.settrace('192.168.99.1', port=2225, stdoutToServer=True, stderrToServer=True, suspend=False)
    listener = Listener('localhost', 'root', 'P@ssword')
    publisher = AMQPPublisher('localhost', 'root', 'P@ssword', 'event', 'event.created', 'on_event_created',
                              create_scoped_session(configuration["db_config"]))
    publisher.start()
    listener.start()
    listener.join()


main()
