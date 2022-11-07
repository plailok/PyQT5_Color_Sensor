import enum
from typing import List, Optional, Tuple

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtSerialPort import QSerialPort

DeviceData = Optional[List[float]]
MeasurementData = Tuple[QColor, DeviceData]


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

    def single_measurement(self, color: QColor) -> MeasurementData:
        self._transport.measure(color)
        while self._transport.state is self._transport.State.MEASURE:
            pass
        data = self._transport._data
        return color, data

    def spectr_measurement(self, step: int, value: int, saturation: int) -> List[MeasurementData]:
        hsv_spectr = (QColor.fromHsv(h, value, saturation) for h in range(0, 360, step))
        return [
            self.single_measurement(color) for color in hsv_spectr
        ]

    def calibrate(self) -> MeasurementData:
        try:
            self._transport.calibrate()
        except Exception as exc:
            print(exc)
        else:
            data = self._transport._data
            return QColor(254, 254, 254), data

    def get_serial(self):
        return self._transport.serial

    @property
    def transport(self):
        return self._transport
