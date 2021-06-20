import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)

from controller import (
    DeviceController,
    DeviceTransport,
)
from .widget_color_setting import ColorSettings
from .widget_left_panel import LeftPanel
from .widget_right_panel import RightPanel


class SensorMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # => SETTINGS
        self.__create_thread()
        self.__set_and_place_widgets()
        self.__set_buttons()
        self.__set_custom()
        # => WIDGETS TO CONTROL
        self.color_values = self.color.color
        self.indicator = self.left.ui.respondLineEdit
        self.current_port = self.left.ui.comPortComboBox.currentText


    def change_indicator_color(self, color):
        """
        Possible color for method:
            gray, black, green, red, blue
        :param color: string
        :return:
        """
        self.indicator.setStyleSheet(f"color:{color}")

    def __set_buttons(self):
        self.left.ui.connectButton.clicked.connect(self.connect)
        self.left.ui.ethalonButton.clicked.connect(self.reference_measure)
        self.left.ui.singleButton.clicked.connect(self.single_measure)
        self.left.ui.multiButton.clicked.connect(self.spectrum_measurement)
        # self.left.ui.startButton.clicked.connect(self.connect)

    def spectrum_measurement(self):
        result = self.device.spectr_measurement()
        print(result)
        for color, values in result:
            print(values)

    def reference_measure(self):
        color, result = self.device.calibrate()
        self.right.set_list_value(result)

    def single_measure(self):
        name = self.device.get_serial()
        name.portName()
        color = self.color_values
        color, result = self.device.single_measurement(color)
        sample = 'Sample'
        result.insert(0, sample)
        self.right.set_list_value(result)
        time.sleep(1)
        self.device.turn_off_led()

    def connect(self):
        serial = self.current_port()
        mask = self.left.ui.portComboBox.currentText()
        port = f'{serial}:{mask}'
        is_connected = self.device.connect(serial)
        self.indicator.setStyleSheet('color:green')

    def disconnect(self):
        self.device.disconnect()

    def __set_custom(self):
        self.setGeometry(300, 100, 1000, 600)
        self.setWindowTitle("To_Test")
        self.setCentralWidget(self.holder)

    def __create_thread(self):
        self.thread = QThread(self)
        self.serial = QSerialPort()
        self.device = DeviceController(DeviceTransport(self.serial))
        self.device.moveToThread(self.thread)
        self.thread.start()

    def __set_and_place_widgets(self):
        """
        Create an important QWidgets and place them on right position.
            self.holder -> Holder for rest QWidgets
            self.left -> Panel with buttons and COMPort ComboBox
            self.color -> Panel for control light source
        :return:
        """
        self.holder = QtWidgets.QWidget()
        self.left = LeftPanel(parent=self)
        self.color = ColorSettings()
        self.right = RightPanel()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.left, 4)
        self.v_layout.addWidget(self.color, 2)
        self.h_layout.addLayout(self.v_layout, 1)
        self.h_layout.addWidget(self.right, 3)
        self.holder.setLayout(self.h_layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = SensorMainWindow()
    application.show()
    sys.exit(app.exec())
