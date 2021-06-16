import sys

from PyQt5 import QtWidgets
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)

from controller import (
    DeviceController,
    DeviceTransport,
)
from widget_color_setting import ColorSettings
from widget_left_panel import LeftPanel
from widget_right_panel import RightPanel


class SensorMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.serial = QSerialPort()
        self.device = DeviceController(DeviceTransport(self.serial))
        self.__set_and_place_widgets()
        self.__set_buttons()
        self.setGeometry(300, 100, 1000, 600)
        self.setWindowTitle("To_Test")
        self.setCentralWidget(self.holder)
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
        self.left.ui.ethalonButton.clicked.connect(self.ethalon_measure)
        self.left.ui.singleButton.clicked.connect(self.single_measure)
        # self.left.ui.multiButton.clicked.connect(self.connect)
        # self.left.ui.startButton.clicked.connect(self.connect)

    def ethalon_measure(self):
        self.device.calibrate()

    def single_measure(self):
        name = self.device.get_serial()
        name.portName()
        color = self.color_values
        result = self.device.single_measurement(color)

    def connect(self):
        serial = self.current_port()
        mask = self.left.ui.portComboBox.currentText()
        port = f'{serial}:{mask}'
        self.device.connect(port)
        self.indicator.setStyleSheet('color:green')

    def disconnect(self):
        self.device.disconnect()

    def __set_and_place_widgets(self):
        """
        Create an important QWidgets and place them on right position.
            self.holder -> Holder for rest QWidgets
            self.left -> Panel with buttons and COMPort ComboBox
            self.color -> Panel for control light source
        :return:
        """
        self.holder = QtWidgets.QWidget()
        self.left = LeftPanel(serial=QSerialPort(), parent=self)
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
