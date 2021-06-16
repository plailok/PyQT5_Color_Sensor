import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox

from .color_settings import Ui_Form as WidgetColorSettings


class ColorSettings(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent if parent else None
        self.ui = WidgetColorSettings()
        self.ui.setupUi(self)
        self.color = QColor(
            self.ui.RspinBox.value(),
            self.ui.GspinBox.value(),
            self.ui.BspinBox.value()
        )
        self.__set_spin_boxes()

    def get_current_color(self) -> QColor:
        return self.color

    def __set_spin_boxes(self):
        self.ui.RspinBox.valueChanged.connect(self.__on_change_r)
        self.ui.GspinBox.valueChanged.connect(self.__on_change_g)
        self.ui.BspinBox.valueChanged.connect(self.__on_change_b)
        self.ui.HSpinBox.valueChanged.connect(self.__on_change_h)
        self.ui.SspinBox.valueChanged.connect(self.__on_change_s)
        self.ui.VspinBox.valueChanged.connect(self.__on_change_v)


    def __on_change_r(self, value: int):
        self.color.setRed(int(value))

    def __on_change_g(self, value: int):
        self.color.setGreen(int(value))

    def __on_change_b(self, value: int):
        self.color.setBlue(int(value))

    def __on_change_h(self, value: int):
        hsv = list(self.color.getHsv())
        hsv[0] = value
        self.color.setHsv(*hsv)
        
    def __on_change_s(self, value: int):
        hsv = list(self.color.getHsv())
        hsv[1] = value
        self.color.setHsv(*hsv)

    def __on_change_v(self, value: int):
        hsv = list(self.color.getHsv())
        hsv[2] = value
        self.color.setHsv(*hsv)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = ColorSettings()
    application.show()
    sys.exit(app.exec())
