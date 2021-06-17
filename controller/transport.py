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
        ERROR = 3

    # signals
    # dataReady = pyqtSignal()

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

    def _wait_data(self):
        self.state = self.State.MEASURE
        if self.serial.waitForReadyRead(1000):
            self._read_data()
        else:
            self.state = self.State.ERROR

    def measure(self, color: QColor):
        print(f'Measure {self.serial}   {type(self.serial)}')
        rgb = color.getRgb()
        data = f"Mr{rgb[0]} g{rgb[1]} b{rgb[2]}\n".encode('ascii')
        self.serial.write(data)
        self._wait_data()

    def calibrate(self):
        self.serial.write(f"C\n".encode('ascii'))
        self._wait_data()

    def _read_data(self):
        if self.serial.read(1) == b'D':
            data = ''
            while self.serial.waitForReadyRead(50):
                data += str(self.serial.readAll(), 'ascii')
            self._data = [float(val) for val in data[:-3].split(',')]
        else:
            self.serial.clear(self.serial.Direction.AllDirections)
            self._data = None
        self.state = self.State.IDLE
        # self.dataReady.emit()


class DeviceController(QObject):

    calibrationDone = pyqtSignal()
    singleMeasureDone = pyqtSignal()
    spectrMeasureDone = pyqtSignal()

    def __init__(self, transport: DeviceTransport, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._transport = transport
        self._data = []

    @property
    def data(self) -> List[MeasurementData]:
        return self._data

    def connect(self, port: str, baudrate: int = 115200) -> bool:
        return self._transport.connect(port, baudrate)

    def disconnect(self):
        self._transport.disconnect()

    def single_measurement(self, color: QColor) -> None:
        self._transport.measure(color)
        data = self._transport._data
        self._data = [(color, data)]
        self.singleMeasureDone.emit()

    def spectr_measurement(self) -> None:
        hsv_spectr = (QColor.fromHsv(h, 255, 255) for h in range(360))
        self._data = [
            self.single_measurement(color) for color in hsv_spectr
        ]
        self.spectrMeasureDone.emit()

    def calibrate(self) -> None:
        self._transport.calibrate()
        data = self._transport._data
        self._data = [(QColor(255, 255, 255), data)]
        self.calibrationDone.emit()

    def get_serial(self):
        return self._transport.serial
