import enum
from typing import List, Optional, Tuple
from PyQt5.QtCore import QObject, pyqtSignal

from reSPECTool_device_transport import DeviceTransport


class DeviceController(QObject):

    def __init__(self, transport: DeviceTransport) -> None:
        super(DeviceController, self).__init__()
        self._transport = transport

    def connect(self, port: str, baudrate: int = 115200) -> bool:
        return self._transport.connect(port, baudrate)

    def disconnect(self):
        self._transport.disconnect()

    def turn_off_led(self):
        return self._transport.turn_off_led()

    def _read_data(self):
        if self.serial.read(1) == b'D':
            data = ''
            while self.serial.waitForReadyRead(50):
                data += str(self.serial.readAll(), 'ascii')
            d = self.serial.readAll()
            self._data = []
            try:
                self._data = [float(value) for value in d[:-4].split(',')]
            except Exception as exc:
                print(exc)
        else:
            self.serial.clear(self.serial.Direction.AllDirections)
            self._data = None
        self.state = self.State.IDLE
        self.dataReady.emit()

    def set_color(self, value: QColor, flag=False):
        """
        Set Specifi
        :param value: QColor
        :param flag: bool;
        :return:
        """
        v = value.getRgb()
        if flag:
            v = value.getHsv()
        data = f"Mr{v[0]} g{v[1]} b{v[2]}\n".encode('ascii')
