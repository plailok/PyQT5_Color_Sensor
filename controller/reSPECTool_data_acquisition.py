import enum
from typing import List, Optional, Tuple, Any
from reSPECTool_control import DeviceController
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtSerialPort import QSerialPort

DeviceData = Optional[List[float]]
MeasurementData = Tuple[QColor, DeviceData]


class DataMeasurer(QObject):
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

    def measure(self, color: QColor):
        rgb = color.getRgb()
        data = f"Mr{rgb[0]} g{rgb[1]} b{rgb[2]}\n".encode('ascii')
        self.serial.write(data)
        self.state = self.State.MEASURE
        if self.serial.waitForReadyRead(10000):
            self._read_data()
        else:
            self.state = self.State.ERROR

    def single_measurement(self, color: QColor) -> MeasurementData:
        """
        Send the color value to sensor
        Get respond from it in form of tuple
        :param color: QColor
        :return:(color,data)
        """
        self._transport.measure(color)
        while self._transport.state is self._transport.State.MEASURE:
            pass
        data = self._transport._data
        return color, data

    def spectra_measurement(self, step: int, value: int, saturation: int) -> List[MeasurementData]:
        hsv_spectra = (QColor.fromHsv(h, value, saturation) for h in range(0, 360, step))
        return [
            self.single_measurement(color) for color in hsv_spectra
        ]


class MyTableSetting(QTableWidget):
    class SETTINGS:
        COLUMNS_COUNT = 19
        ROW_COUNT = 1
        TECHNICAL_NAMES = ['EC_correction_1', 'EC_correction_2', 'black']
        HEADER = ['Sample Name',
                  '410 nm', '435 nm', '460 nm', '485 nm', '510 nm', '535 nm',
                  '560 nm', '585 nm', '610 nm', '645 nm', '680 nm', '705 nm',
                  '730 nm', '760 nm', '810 nm', '860 nm', '900 nm', '940 nm']
        DEFAULT_NAME = f'{datetime.datetime}_output.xlsx'

    def __init__(self, size: tuple = None):
        """

        :param size => size(COLUMN, ROW):
        :param data => data{experiment:
                           {ethalon:[result],
                            measurments:[results]}
                           }:
        """
        super().__init__()
        self.set = size
        # exp_counter - счётчик экспериментов (измерений вида: эталон + несколько измерений)
        self.exp_counter = 0
        self.counter = 1

        # SETTINGS
        if not size:
            self.setColumnCount(self.SETTINGS.COLUMNS_COUNT)
            self.setRowCount(self.SETTINGS.ROW_COUNT)
        else:
            self.setColumnCount(size[0])
            self.setRowCount(size[1])

        self.setHorizontalHeaderLabels(self.SETTINGS.HEADER)
        self.resizeColumnsToContents()
        self.data = None

    def _add_to_dict(self, data: dict):
        """
        :param data in format {ethalon:[result]} or {measurements:[results]}:
        :return:
        """
        if self.data is None:
            self.data = {self.exp_counter: data}
            self.data[self.exp_counter].update({'measurements': []})
            for value in self.data[self.exp_counter].items():
                self._add_to_table_noname(value)
            return
        if 'ethalon' in data.keys():
            self.exp_counter += 1
            self.data.update({self.exp_counter: data})
            self.data[self.exp_counter].update({'measurements': []})
            for value in self.data[self.exp_counter].items():
                self._add_to_table_noname(value)
            return
        if 'measurements' in data.keys() or 'measurements_single' in data.keys():
            if 'measurements' not in self.data[self.exp_counter].keys():
                self.data[self.exp_counter].update({'measurements': []})
            for value in data.values():
                self.data[self.exp_counter]['measurements'].append(value)
                self._add_to_table_noname(('measurements', [value]))
            return
        if 'black' in data.keys():
            if 'black' not in self.data.keys():
                self.data.update(data)
                self._add_to_table_noname(('black', [self.data['black']]))

    def _add_to_table_noname(self, data: tuple):
        """
        :param data in format {ethalon:[result]} or {measurements:[results]}:
        :return:
        """
        if data[0] == 'ethalon':
            self.setItem(self.counter - 1, 0, QTableWidgetItem(f'EC_{self.exp_counter}'))
            self.fill_table(data[1])
            return
        if data[0] == 'measurements':
            experiment_number = len(self.data[self.exp_counter]["measurements"])
            for measurement in data[1]:
                self.setItem(self.counter - 1, 0, QTableWidgetItem(f'Meas{experiment_number}'))
                self.fill_table(measurement)
            return
        if data[0] == 'measurements_single':
            for measurement in data[1]:
                self.setItem(self.counter - 1, 0, QTableWidgetItem(f'Meas_value'))
                self.fill_table(measurement)
            return
        if data[0] == 'black':
            for measurement in data[1]:
                self.setItem(self.counter - 1, 0, QTableWidgetItem('black'))
                self.fill_table(measurement)
        if data[0] == 'EC_correction_1':
            for measurement in data[1]:
                self.setItem(self.counter - 1, 0, QTableWidgetItem('EC_corr'))
                self.fill_table(measurement)
        if 'corr_exp' in data[0]:
            for measurement in data[1]:
                self.setItem(self.counter - 1, 0, QTableWidgetItem(data[0]))
                self.fill_table(measurement)


