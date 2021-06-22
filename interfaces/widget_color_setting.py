import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor

from color_settings import Ui_Form as WidgetColorSettings


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

        self.rgb_spin_boxes = [self.ui.RspinBox, self.ui.GspinBox, self.ui.BspinBox]
        self.rgb_labels = [self.ui.RLabel, self.ui.GLabel, self.ui.BLabel]
        self.hsv_spin_boxes = [self.ui.HSpinBox, self.ui.SspinBox, self.ui.VspinBox]
        self.hsv_labels = [self.ui.HLabel, self.ui.SLabel, self.ui.VLabel]

    def get_current_color(self) -> QColor:
        return self.color

    def set_labels_color(self):
        rgb = list(self.color.getRgb())
        style = f"color:rgb({rgb[0]},{rgb[1]},{rgb[2]});"
        for index in range(3):
            self.rgb_labels[index].setStyleSheet(style)
            self.hsv_labels[index].setStyleSheet(style)

    def set_hsv_spin_boxes(self):
        hsv = list(self.color.getHsv())
        for index, spinbox in enumerate(self.hsv_spin_boxes):
            spinbox.setValue(hsv[index])

    def set_rgb_spin_boxes(self):
        rgb = list(self.color.getRgb())
        for index, spinbox in enumerate(self.rgb_spin_boxes):
            spinbox.setValue(rgb[index])

    def __set_spin_boxes(self):
        self.ui.RspinBox.valueChanged.connect(self.__on_change_r)
        self.ui.GspinBox.valueChanged.connect(self.__on_change_g)
        self.ui.BspinBox.valueChanged.connect(self.__on_change_b)
        self.ui.HSpinBox.valueChanged.connect(self.__on_change_h)
        self.ui.SspinBox.valueChanged.connect(self.__on_change_s)
        self.ui.VspinBox.valueChanged.connect(self.__on_change_v)

    def __on_change_r(self, value: int):
        if self.ui.tabWidget.currentWidget().objectName() == 'rgb':
            self.color.setRed(int(value))
            self.set_hsv_spin_boxes()
            self.set_labels_color()

    def __on_change_g(self, value: int):
        if self.ui.tabWidget.currentWidget().objectName() == 'rgb':
            self.color.setGreen(int(value))
            self.set_hsv_spin_boxes()
            self.set_labels_color()

    def __on_change_b(self, value: int):
        if self.ui.tabWidget.currentWidget().objectName() == 'rgb':
            self.set_hsv_spin_boxes()
            self.color.setBlue(int(value))
            self.set_labels_color()

    def __on_change_h(self, value: int):
        if self.ui.tabWidget.currentWidget().objectName() == 'hsv':
            hsv = list(self.color.getHsv())
            hsv[0] = value
            self.color.setHsv(*hsv)
            self.set_rgb_spin_boxes()
            self.set_labels_color()

    def __on_change_s(self, value: int):
        if self.ui.tabWidget.currentWidget().objectName() == 'hsv':
            hsv = list(self.color.getHsv())
            hsv[1] = value
            self.color.setHsv(*hsv)
            self.set_rgb_spin_boxes()
            self.set_labels_color()

    def __on_change_v(self, value: int):
        if self.ui.tabWidget.currentWidget().objectName() == 'hsv':
            hsv = list(self.color.getHsv())
            hsv[2] = value
            self.color.setHsv(*hsv)
            self.set_rgb_spin_boxes()
            self.set_labels_color()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = ColorSettings()
    application.show()
    sys.exit(app.exec())
