import abc
import logging
import os
from multiprocessing import Process, Queue, Event
from typing import Any

import pyshark
import time
from pyshark import FileCapture
from pyshark.packet.packet import Packet


class PacketReader(abc.ABC, Process):
    def __init__(self, queue_: Queue, *args: Any, **kwargs: Any):
        super().__init__()
        self._queue = queue_
        self._logger = logging.getLogger(self.__class__.__name__)
        self._stop_event = Event()

    def stop_read(self, timeout: int):
        # self._logger.info(f"Остановка {self.__class__.__name__}")
        self._stop_event.set()
        self.join(timeout)
        self.terminate()


class PcapReader(PacketReader):
    def __init__(self, filename: str, queue_: Queue, *args: Any, **kwargs: Any):
        self.pcap_filename = filename
        super().__init__(queue_)

    def run(self, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(f"Read traffic from {self.pcap_filename}")
        capture: FileCapture = pyshark.FileCapture(self.pcap_filename)
        for packet in capture:
            self._queue.put_nowait(packet)
        self._logger.debug(f"End read traffic from {self.pcap_filename}")


class InterfaceReader(PacketReader):
    def __init__(self, interface_name: str, queue_: Queue, *args: Any, **kwargs: Any):
        self.interface_name = interface_name
        super().__init__(queue_)

    def run(self, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(f"Listening traffic on {self.interface_name}")
        capture: pyshark.LiveCapture = pyshark.LiveCapture(interface=self.interface_name)
        capture.apply_on_packets(callback=self._callback)

    def _callback(self, packet: Packet):
        self._queue.put_nowait(packet)
