from multiprocessing import Queue

from analyzer.packet_analyzer import PacketAnalyzer
from analyzer.reader import PcapReader


def main():
    queue_ = Queue()
    reader = PcapReader('sql_test.pcap', queue_)
    packet_analyzer = PacketAnalyzer(queue_)
    packet_analyzer.start()
    reader.start()
    reader.join()
    packet_analyzer.join()
    pass


if __name__ == '__main__':
    main()
