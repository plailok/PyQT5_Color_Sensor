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
    dataReady = pyqtSignal()
    _progressBar = pyqtSignal(tuple)

    def __init__(self, serial: QSerialPort) -> None:
        super().__init__()
        self.serial = serial
        self._data = []
        self._color = None
        self.state = self.State.IDLE

    def connect(self, port: str, baudrate: int = 115200) -> bool:
        self.serial.setBaudRate(baudrate)
        self.serial.setPortName(port)
        return self.serial.open(self.serial.OpenModeFlag.ReadWrite)

    def disconnect(self):
        self.serial.close()

    def turn_off_led(self):
        sets = [f"Mr0 g50 b50\n", 'f"Mr1 g1 b1\n"']
        for set in range(2):
            data = sets[set].encode('ascii')
            try:
                self.serial.write(data)
            except Exception as exc:
                print(exc)

    def measure(self, color: QColor):
        rgb = color.getRgb()
        data = f"Mr{rgb[0]} g{rgb[1]} b{rgb[2]}\n".encode('ascii')
        self.serial.write(data)
        self.state = self.State.MEASURE
        if self.serial.waitForReadyRead(10000):
            self._read_data()
        else:
            self.state = self.State.ERROR

    def calibrate(self):
        self.serial.write(f"Mr255 g255 b255\n".encode('ascii'))
        self.state = self.State.MEASURE

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

    @property
    def progressBar(self):
        return self._progressBar


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

    def spectr_measurement(self) -> List[MeasurementData]:
        hsv_spectr = (QColor.fromHsv(h, 255, 255) for h in range(0, 360, 30))
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
