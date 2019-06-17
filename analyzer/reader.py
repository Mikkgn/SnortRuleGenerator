import abc
import logging
from multiprocessing import Process, Queue, Event
from typing import Any

import pyshark
from pyshark import FileCapture


class PacketReader(abc.ABC, Process):
    def __init__(self, queue_: Queue):
        super().__init__()
        self._queue = queue_
        self._logger = logging.getLogger(self.__class__.__name__)
        self._stop_event = Event()


class PcapReader(PacketReader):
    def __init__(self, filename: str, queue_: Queue):
        self.pcap_filename = filename
        super().__init__(queue_)

    def run(self, *args: Any, **kwargs: Any):
        self._logger.debug(f"Read traffic from {self.pcap_filename}")
        capture: FileCapture = pyshark.FileCapture(self.pcap_filename)
        for packet in capture:
            self._queue.put_nowait(packet)
        self._logger.debug(f"End read traffic from {self.pcap_filename}")


class InterfaceReader(PacketReader):
    def __init__(self, interface_name: str, queue_: Queue):
        self.interface_name = interface_name
        super().__init__(queue_)

    def run(self, *args: Any, **kwargs: Any):
        self._logger.debug(f"Listening traffic on {self.interface_name}")
        capture: pyshark.LiveCapture = pyshark.LiveCapture(self.interface_name)
        while not self._stop_event.is_set():
            for packet in capture.sniff_continuously():
                self._queue.put_nowait(packet)