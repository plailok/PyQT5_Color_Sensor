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
from widget_color_setting import ColorSettings
from widget_left_panel import LeftPanel
from widget_right_panel import RightPanel


class SensorMainWindowSettings(QtWidgets.QMainWindow):
    class Positioner:
        """
        The class is designed to permute the result by wavelength
        wavelengths in order:
        0 - name; 13 - 410, 14 - 435, 15 - 460, 16 - 485, 17 - 510
            18 - 535, 7 - 560, 8 - 585, 1 - 610, 9 - 645, 2 - 680,
            10 - 705, 3 - 730, 4 - 760, 5 - 810, 6 - 860, 11 - 900
            12 - 940
        """
        correct_position = [0, 13, 14, 15, 16, 17,
                            18, 7, 8, 1, 9, 2, 10,
                            3, 4, 5, 6, 11, 12]

        def get_corrected(self, result: list) -> list:
            return [result[index] for index in self.correct_position]

    def __init__(self):
        super().__init__()
        # => SETTINGS
        self.__create_thread()
        self.__set_and_place_widgets()
        self.__set_buttons()
        self.__set_custom()
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
        self.__change_buttons_availability(False)
        result = self.device.spectr_measurement()
        self.__change_buttons_availability(True)
        for color, value in result:
            h, s, v, _ = color.getHsv()
            sample = f'S{h}'
            value.insert(0, sample)
            self.right.set_list_value(value)

    def reference_measure(self):
        """
        Reference measurement
        :return:
        """
        cur_color = self.color_values.getRgb()
        self.color_values.setRgb(254, 254, 254)
        self.single_measure(is_calibrate=True, color=self.color_values)
        self.color_values.setRgb(*cur_color)
        self.device.turn_off_led()

    def single_measure(self, is_calibrate: bool = None, color=None):
        """
        is_calibrate == True & color is not None => Etalon measurement ( color = (255, 255, 255) )
        is_calibrate == False & color is None
        is_calibrate is None & color is None => Normal single measurement
        :param is_calibrate:
        :param color:
        :return:
        """
        self.__change_buttons_availability(False)
        if is_calibrate is True and color:
            rgb_color = color
            color, result = self.device.single_measurement(rgb_color)
            set_name = 'EC'
        elif is_calibrate is False:
            rgb_color = self.color_values
            color, result = self.device.single_measurement(rgb_color)
            set_name = self.left.ui.lineEdit.text()
            if set_name == '':
                set_name = 'Sample'
        else:
            rgb_color = self.color_values
            color, result = self.device.single_measurement(rgb_color)
            set_name = 'Single'
        self.device.turn_off_led()
        result.insert(0, set_name)
        corrected_result = self.positioner.get_corrected(result)
        self.right.set_list_value(corrected_result)
        time.sleep(3)
        self.__change_buttons_availability(True)
        self.device.turn_off_led()

    def connect(self):
        serial = self.current_port()
        try:
            self.device.connect(serial)
        except Exception as exc:
            print(exc)
            self.indicator.setText('Error')
            self.indicator.setStyleSheet('color:red')
            self.__change_buttons_availability(False)
            return
        else:
            self.indicator.setText('Connected')
            self.indicator.setStyleSheet('color:green')
            self.__change_buttons_availability(True)

    def disconnect(self):
        self.device.disconnect()
        self.indicator.setText('Disconnected')
        self.indicator.setStyleSheet('color:black')

    def __set_buttons(self):
        self.left.ui.connectButton.clicked.connect(self.connect)
        self.left.ui.ethalonButton.clicked.connect(self.reference_measure)
        self.left.ui.singleButton.clicked.connect(self.single_measure)
        self.left.ui.multiButton.clicked.connect(self.spectrum_measurement)
        self.device._transport._progressBar.connect(self.__progress_bar_change)

    def __change_buttons_availability(self, is_valid: bool):
        self.left.ui.singleButton.setEnabled(is_valid)
        self.left.ui.ethalonButton.setEnabled(is_valid)
        self.left.ui.startButton.setEnabled(is_valid)
        self.left.ui.multiButton.setEnabled(is_valid)

    def __progress_bar_change(self, color):
        self.left.ui.progressBar.show()
        h, __, ___, _ = color
        bar_value = h // 3.6
        self.left.ui.progressBar.setValue(bar_value)
        if h == 359:
            self.left.ui.progressBar.hide()

    def __set_custom(self):
        self.setGeometry(300, 100, 1000, 600)
        self.setWindowTitle("To_Test")
        self.setCentralWidget(self.holder)
        self.left.ui.progressBar.hide()

    def __create_thread(self):
        self.thread = QThread()
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
    application = SensorMainWindowSettings()
    application.show()
    sys.exit(app.exec())
