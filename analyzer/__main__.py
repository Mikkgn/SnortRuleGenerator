
from multiprocessing import Queue

from analyzer.config import configuration
from analyzer.db.engine import wait_db, init_db
from analyzer.packet_analyzer import PacketAnalyzer
from analyzer.reader import PcapReader


def main():
    queue_ = Queue()
    wait_db(**configuration["db_config"])
    init_db(configuration["db_config"])
    # import sys
    # sys.path.append('./pydevd-pycharm.egg')
    # import pydevd_pycharm
    # pydevd_pycharm.settrace('192.168.99.1', port=2225, stdoutToServer=True, stderrToServer=True, suspend=False)
    packet_analyzer = PacketAnalyzer(queue_)
    reader = PcapReader('test.pcap', queue_)
    packet_analyzer.start()
    reader.start()
    reader.join()
    packet_analyzer.join()
    pass


main()
