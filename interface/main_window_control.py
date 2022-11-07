import random
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

try:
    from interface.main_window_settings import SensorMainWindowSettings
    from interface.GUI_setting.widget_chose_step_dialog import ChoseStepDialog
    from interface.GUI_setting.widget_color_setting import ColorSettings
    from interface.GUI_setting.widget_left_panel import LeftPanel
    from interface.GUI_setting.widget_right_panel import RightPanel
except ModuleNotFoundError:
    from .interface.main_window_settings import SensorMainWindowSettings
    from .interface.GUI_py.widget_chose_step_dialog import ChoseStepDialog
    from .interface.GUI_py.widget_color_setting import ColorSettings
    from .interface.GUI_py.widget_left_panel import LeftPanel
    from .interface.GUI_py.widget_right_panel import RightPanel


class SensorMainWindowControl(SensorMainWindowSettings):

    def __init__(self):
        super().__init__()
        # => MAIN
        self.color_values = self.color.color
        self.indicator = self.left.ui.respondLineEdit
        self.current_port = self.left.ui.comPortComboBox.currentText
        self.positioner = self.Positioner()

    def spectrum_measurement(self):
        """
        Measure for each value for HSV circle
        :return:
        """
        dialog = ChoseStepDialog()
        dialog.exec()
        if dialog.rejected:
            pass
        elif dialog.accepted:
            if dialog.is_modified:
                h, s, v = dialog.get_hsv()
            else:
                h = dialog.get_h()
                s, v = 255, 255
            self._change_buttons_availability(False)
            result = self.device.spectr_measurement(step=h, value=v, saturation=s)
            self._change_buttons_availability(True)
            for color, value in result:
                h, s, v, _ = color.getHsv()
                sample_type = 'measurements'
                value.insert(0, sample_type)
                self.right.ui.tableWidget.add(data=value)

    def reference_measure(self):
        """
        Reference measurement
        """
        cur_color = self.color_values.getRgb()
        self.color_values.setRgb(254, 254, 254)
        color, result = self.device.single_measurement(color=self.color_values)
        corrected_result = self.positioner.get_corrected(result)
        corrected_result.insert(0, 'ethalon')
        self.color_values.setRgb(*cur_color)
        self.right.ui.tableWidget.add(data=corrected_result)  # add corrected result to the table and to the memory
        self._change_buttons_availability(True)

    def single_measure(self, color=None, isblack=False):
        """
        is_calibrate == True & color is not None => Etalon measurement ( color = (255, 255, 255) )
        is_calibrate == False & color is None =>
        is_calibrate is None & color is None => Normal single measurement
        :param isblack:
        :param color:
        :return:
        """
        self._change_buttons_availability(False)
        color, result = self.device.single_measurement(self.color_values)
        corrected_result = self.positioner.get_corrected(result=result)
        set_name = 'black' if isblack is True else 'measurements'
        corrected_result.insert(0, set_name)
        self.right.ui.tableWidget.add(data=corrected_result)  # add corrected result to the table and to the memory
        self._change_buttons_availability(True)

    def black_measure(self):
        """
        Reference measurement
        :return:
        """
        cur_color = self.color_values.getRgb()
        self.color_values.setHsv(0, 0, 0)
        self.single_measure(isblack=True, color=self.color_values)
        self.color_values.setRgb(*cur_color)

    def connect(self):
        serial = self.current_port()
        try:
            self.device.connect(serial)
        except Exception as exc:
            print(exc)
            self.indicator.setText('Error')
            self.indicator.setStyleSheet('color:red')
            self._change_buttons_availability(False)
            return
        else:
            self.indicator.setText('Connected')
            self.indicator.setStyleSheet('color:green')
            self._change_buttons_availability(True)
            self.left.ui.connectButton.setText('DISCONNECT')
            self.left.ui.connectButton.clicked.connect(self.disconnect)

    def disconnect(self):
        if self.device:
            self.device.disconnect()
            self.indicator.setText('Disconnected')
            self.indicator.setStyleSheet('color:gray')
            self._change_buttons_availability(False)
            self.left.ui.connectButton.setText('CONNECT')
            self.left.ui.connectButton.clicked.connect(self.connect)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = SensorMainWindowControl()
    application.show()
    sys.exit(app.exec())
