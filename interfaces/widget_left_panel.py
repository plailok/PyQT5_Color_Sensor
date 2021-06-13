import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QIODevice
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort

from .left_panel import Ui_Form as WidgetLeftPanel


class LeftPanel(QtWidgets.QWidget):

    def __init__(self, serial: QSerialPort, parent=None):
        super().__init__()
        self.parent = parent if parent else None
        self.ui = WidgetLeftPanel()
        self.ui.setupUi(self)
        self.serial = serial

        self.__set_comport_combobox()
        self.__setup_buttons()

    def __setup_buttons(self):
        self.ui.refreshButton.clicked.connect(self.__refresh_pressed)
        self.ui.connectButton.clicked.connect(self.__connect_pressed)
        self.ui.ethalonButton.clicked.connect(self.__reference_pressed)
        self.ui.startButton.clicked.connect(self.__start_pressed)
        self.ui.singleButton.clicked.connect(self.__single_pressed)
        self.ui.multiButton.clicked.connect(self.__multi_pressed)

    def __refresh_pressed(self):
        while self.ui.comPortComboBox.count() != 0:
            self.ui.comPortComboBox.removeItem(0)
        self.__set_comport_combobox()

    def __connect_pressed(self):
        try:
            baud = int(self.ui.portComboBox.currentText())
            name = self.ui.comPortComboBox.currentText()
            self.serial.setBaudRate(baud)
            self.serial.setPortName(name)
        except Exception as exc:
            print(exc)

    def __reference_pressed(self):
        while self.ui.comPortComboBox.count() != 0:
            self.ui.comPortComboBox.removeItem(0)
        self.__set_comport_combobox()

    def __single_pressed(self):
        print('single') if not self.parent else None

    def __start_pressed(self):
        print('start') if not self.parent else None
        pass

    def __multi_pressed(self):
        print('multi') if not self.parent else None
        pass

    def __set_comport_combobox(self):
        port_info = QSerialPortInfo()
        available_ports = port_info.availablePorts()
        for port in available_ports:
            self.ui.comPortComboBox.addItem(port.portName())
        if not self.ui.comPortComboBox.children():
            self.ui.comPortComboBox.setEnabled(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = LeftPanel()
    application.show()
    sys.exit(app.exec())
