import sys

from PyQt5 import QtWidgets
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)

from .widget_color_setting import ColorSettings
from .widget_left_panel import LeftPanel
from .widget_right_panel import RightPanel


class SensorMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.serial = QSerialPort()
        self.__set_and_place_widgets()
        self.setGeometry(300, 100, 1000, 600)
        self.setWindowTitle("To_Test")
        self.setCentralWidget(self.holder)

    def __set_and_place_widgets(self):
        """
        Create an important QWidgets and place them on right position.
            self.holder -> Holder for rest QWidgets
            self.left -> Panel with buttons and COMPort ComboBox
            self.color -> Panel for control light source
        :return:
        """
        self.holder = QtWidgets.QWidget()
        self.left = LeftPanel(serial=QSerialPort())
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
