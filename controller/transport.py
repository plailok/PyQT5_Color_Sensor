import enum
from typing import List, Optional, Tuple

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtSerialPort import QSerialPort

DeviceData = Optional[List[float]]
MeasurementData = Tuple[QColor, DeviceData]


class DeviceTransport(QObject):
    class State(enum.Enum):
        IDLE = 1
        MEASURE = 2

    # signals
    dataReady = pyqtSignal()

    def __init__(self, serial: QSerialPort) -> None:
        super().__init__()
        self.serial = serial
        # self.serial.readyRead.connect(self._read_data)
        self._data: List[float] = []
        self._color = None
        self.state = self.State.IDLE

    def connect(self, port: str, baudrate: int = 115200) -> bool:
        print(port)
        self.serial.setBaudRate(baudrate)
        self.serial.setPortName(port)
        return self.serial.open(self.serial.OpenModeFlag.ReadWrite)

    def disconnect(self):
        self.serial.close()

    def measure(self, color: QColor):
        print(f'Measure {self.serial}   {type(self.serial)}')
        rgb = color.getRgb()
        data = f"Mr{rgb[0]} g{rgb[1]} b{rgb[2]}\n".encode('ascii')
        self.serial.write(data)
        self.state = self.State.MEASURE
        if self.serial.waitForReadyRead(1000):
            self._read_data()

    def calibrate(self):
        self.serial.write(f"C\n".encode('ascii'))
        self.state = self.State.MEASURE

    def _read_data(self):
        if self.serial.read(1) == b'D':
            data = ''
            while self.serial.waitForReadyRead(50):
                data += str(self.serial.readAll(), 'ascii')
            self._data = [float(val) for val in data.split(',')]
        else:
            self.serial.clear(self.serial.Direction.AllDirections)
            self._data = None
        self.state = self.State.IDLE
        self.dataReady.emit()


class DeviceController(QObject):

    def __init__(self, transport: DeviceTransport) -> None:
        self._transport = transport

    def connect(self, port: str, baudrate: int = 115200) -> bool:
        return self._transport.connect(port, baudrate)

    def disconnect(self):
        self._transport.disconnect()

    def single_measurement(self, color: QColor) -> MeasurementData:
        self._transport.measure(color)
        while self._transport.state is self._transport.State.MEASURE:
            pass
        data = self._transport._data
        return color, data

    def spectr_measurement(self) -> List[MeasurementData]:
        hsv_spectr = (QColor.fromHsv(h, 255, 255) for h in range(360))
        return [
            self.single_measurement(color) for color in hsv_spectr
        ]

    def calibrate(self) -> MeasurementData:
        self._transport.calibrate()
        while self._transport.state is self._transport.State.MEASURE:
            pass
        data = self._transport._data
        return QColor(255, 255, 255), data

    def get_serial(self):
        return self._transport.serial
