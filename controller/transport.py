from typing import List, Optional, Tuple
import enum
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSerialPort import QSerialPort
from colour import Color

DeviceData = Optional[List[float]]
MeasurementData = Tuple[Color, DeviceData]


class DeviceTransport:

    class State(enum.Enum):
        IDLE = 1 
        MEASURE = 2
    
    #signals
    dataReady = pyqtSignal()

    def __init__(self, serial: QSerialPort) -> None:
        self.serial = serial
        self.serial.readyRead.connect(self._read_data)
        self._data : List[float] = []
        self._color = None
        self.state = self.State.IDLE

    def connect(self, port: str) -> bool:
        return self.serial.open(self.serial.OpenModeFlag.ReadWrite)

    def disconnect(self):
        self.serial.close()

    def measure(self, color: Color):
        rgb = [int(val * 255) for val in color.get_rgb()]
        self.serial.write(f"Mr{rgb[0]} g{rgb[1]} b{color.rgb[2]}\n".encode('ascii'))
        self.state = self.State.MEASURE

    def calibrate(self):
        self.serial.write(f"C\n".encode('ascii'))
        self.state = self.State.MEASURE

    def _read_data(self):
        if self.serial.read(1) == b'D':
            self._data = [float(val) for val in str(self.serial.readAll()).split(',')]
        else:
            self.serial.clear(self.serial.Direction.AllDirections)
            self._data = None
        self.state = self.State.IDLE
        self.dataReady.emmit()


class DeviceController:

    def __init__(self, transport: DeviceTransport) -> None:
        self._transport = transport

    def connect(self, port: str) -> bool:
        return self._transport.connect(port)

    def disconnect(self):
        self._transport.disconnect()

    def single_measurement(self, color: Color) -> MeasurementData:
        self._transport.measure(color)
        while self._transport.state is self._transport.State.MEASURE:
            pass
        data = self._transport._data
        return color, data

    def spectr_measurement(self) -> List[MeasurementData]:
        hsv_spectr = (Color(hsl=(h/360, 1, 1)) for h in range(360))
        return [
            self.single_measurement(color) for color in hsv_spectr
        ]

    def calibrate(self) -> MeasurementData:
        self._transport.calibrate()
        while self._transport.state is self._transport.State.MEASURE:
            pass
        data = self._transport._data
        return Color(rgb=(1, 1, 1)), data