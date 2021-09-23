import sys

from PyQt5 import QtWidgets
from PyQt5.QtSerialPort import QSerialPortInfo

try:
    from left_panel import Ui_Form as WidgetLeftPanel
except ModuleNotFoundError:
    from .left_panel import Ui_Form as WidgetLeftPanel


class LeftPanel(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent if parent else None
        self.ui = WidgetLeftPanel()
        self.ui.setupUi(self)
        self.__set_comport_combobox()
        self.__setup_buttons()

    def __setup_buttons(self):
        self.ui.refreshButton.clicked.connect(self.__refresh_pressed)
        self.ui.singleButton.clicked.connect(self.__single_pressed)
        self.ui.multiButton.clicked.connect(self.__multi_pressed)

    def __refresh_pressed(self):
        while self.ui.comPortComboBox.count() != 0:
            self.ui.comPortComboBox.removeItem(0)
        self.__set_comport_combobox()

    def __single_pressed(self):
        print('single') if not self.parent else None

    def __multi_pressed(self):
        print('multi') if not self.parent else None
        pass

    def __ec_1_pressed(self):
        print('ec_1') if not self.parent else None

    def __ec_2_pressed(self):
        print('ec2_pressed') if not self.parent else None

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
