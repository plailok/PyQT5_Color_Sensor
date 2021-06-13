import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox

from .color_settings import Ui_Form as WidgetColorSettings


class ColorSettings(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent if parent else None
        self.ui = WidgetColorSettings()
        self.ui.setupUi(self)
        self.values = {'hsv': [index.value() for index in self.ui.hsv.children() if
                               type(index) == QSpinBox or type(index) == QDoubleSpinBox],
                       'rgb': [index.value() for index in self.ui.rgb.children() if type(index) == QSpinBox]}
        self.__set_spin_boxes()

    def get_current_values(self):
        return self.values[self.ui.tabWidget.currentWidget().objectName()]

    def __set_spin_boxes(self):
        self.ui.RspinBox.textChanged.connect(self.__on_change_r)
        self.ui.GspinBox.textChanged.connect(self.__on_change_g)
        self.ui.BspinBox.textChanged.connect(self.__on_change_b)
        self.ui.HDoubleSpinBox.textChanged.connect(self.__on_change_h)
        self.ui.SspinBox.textChanged.connect(self.__on_change_s)
        self.ui.RspinBox.textChanged.connect(self.__on_change_v)

    def __on_change_r(self, value: str):
        self.values['rgb'][0] = int(value)

    def __on_change_g(self, value: str):
        self.values['rgb'][1] = int(value)

    def __on_change_b(self, value: str):
        self.values['rgb'][2] = int(value)

    def __on_change_h(self, value: str):
        self.values['hsv'][0] = float(value)

    def __on_change_s(self, value: str):
        self.values['hsv'][1] = int(value)

    def __on_change_v(self, value: str):
        self.values['hsv'][2] = int(value)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = ColorSettings()
    application.show()
    sys.exit(app.exec())
