from analyzer.config import configuration
from analyzer.listener import Listener
from common.db.engine import wait_db, init_db


def main():
    wait_db(**configuration["db_config"])
    init_db(configuration["db_config"])
    # import sys
    # sys.path.append('./pydevd-pycharm.egg')
    # import pydevd_pycharm
    # pydevd_pycharm.settrace('192.168.99.1', port=2225, stdoutToServer=True, stderrToServer=True, suspend=False)
    listener = Listener('localhost', 'root', 'P@ssword')
    listener.start()
    listener.join()


main()
