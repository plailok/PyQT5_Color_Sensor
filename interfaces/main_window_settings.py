import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)

from widget_color_setting import ColorSettings
from widget_left_panel import LeftPanel
from widget_right_panel import RightPanel


class SensorMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.__set_and_place_widgets()
        self.setGeometry(300, 100, 1000, 600)
        self.setWindowTitle("To_Test")
        self.setCentralWidget(self.holder)
        self.color_values = self.color.values
        self.indicator = self.left.ui.respondLineEdit
        self.serial_port = self.left.serial

    def change_indicator_color(self, color):
        """
        Possible color for method:
            gray, black, green, red, blue
        :param color: string
        :return:
        """
        self.indicator.setStyleSheet(f"color:{color}")

    def __set_and_place_widgets(self):
        """
        Create an important QWidgets and place them on right position.
            self.holder -> Holder for rest QWidgets
            self.left -> Panel with buttons and COMPort ComboBox
            self.color -> Panel for control light source
        :return:
        """
        self.holder = QtWidgets.QWidget()
        self.left = LeftPanel()
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
