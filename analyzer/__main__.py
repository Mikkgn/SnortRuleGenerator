from multiprocessing import Queue

from analyzer.config import configuration
from analyzer.db.engine import wait_db, init_db
from analyzer.packet_analyzer import PacketAnalyzer
from analyzer.reader import PcapReader


def main():
    queue_ = Queue()
    wait_db(**configuration["db_config"])
    init_db(configuration["db_config"])
    packet_analyzer = PacketAnalyzer(queue_)
    reader = PcapReader('test.pcap', queue_)
    packet_analyzer.start()
    reader.start()
    reader.join()
    packet_analyzer.join()
    pass


main()
