import enum
from typing import List, Optional, Tuple
from reSPECTool_device_transport import DeviceTransport
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtSerialPort import QSerialPort

DeviceData = Optional[List[float]]
MeasurementData = Tuple[QColor, DeviceData]


class DeviseCalibrator(DeviceController):
    def __init__(self, transport: DeviceTransport):
        super(DeviseCalibrator, self).__init__(transport=transport)

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
