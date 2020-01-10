from analyzer.config import configuration
from analyzer.listener import Listener


def main():
    # import sys
    # sys.path.append('./pydevd-pycharm.egg')
    # import pydevd_pycharm
    # pydevd_pycharm.settrace('192.168.99.1', port=2225, stdoutToServer=True, stderrToServer=True, suspend=False)
    listener = Listener(**configuration['rabbitmq_config'])
    listener.start()
    listener.join()


main()
