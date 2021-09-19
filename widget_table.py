from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QErrorMessage
import sys
from PyQt5.QtWidgets import QApplication
from math import fabs


class MyTableSetting(QTableWidget):
    class SETTINGS:
        COLUMNS_COUNT = 19
        ROW_COUNT = 1
        TECHNICAL_NAMES = ['EC_correction_1', 'EC_correction_2', 'black']
        HEADER = ['Sample Name',
                  '410 nm', '435 nm', '460 nm', '485 nm', '510 nm', '535 nm',
                  '560 nm', '585 nm', '610 nm', '645 nm', '680 nm', '705 nm',
                  '730 nm', '760 nm', '810 nm', '860 nm', '900 nm', '940 nm']

    def __init__(self, size: tuple = None):
        """

        :param size => size(COLUMN, ROW):
        :param data => data{experiment:
                           {ethalon:[result],
                            measurments:[results]}
                           }:
        """
        super().__init__()
        self.set = size
        # exp_counter - счётчик экспериментов (измерений вида: эталон + несколько измерений)
        self.exp_counter = 0
        self.counter = 1

        # SETTINGS
        if not size:
            self.setColumnCount(self.SETTINGS.COLUMNS_COUNT)
            self.setRowCount(self.SETTINGS.ROW_COUNT)
        else:
            self.setColumnCount(size[0])
            self.setRowCount(size[1])

        self.setHorizontalHeaderLabels(self.SETTINGS.HEADER)
        self.resizeColumnsToContents()
        self.data = None

    def _add_to_dict(self, data: dict):
        """
        :param data in format {ethalon:[result]} or {measurements:[results]}:
        :return:
        """
        if self.data is None:
            self.data = {self.exp_counter: data}
            for value in self.data[self.exp_counter].items():
                self._add_to_table_noname(value)
            return
        if 'ethalon' in data.keys():
            self.exp_counter += 1
            self.data.update({self.exp_counter: data})
            self.data[self.exp_counter].update({'measurements': []})
            for value in self.data[self.exp_counter].items():
                self._add_to_table_noname(value)
            return
        if 'measurements' in data.keys() or 'measurements_single' in data.keys():
            if 'measurements' not in self.data[self.exp_counter].keys():
                self.data[self.exp_counter].update({'measurements': []})
            for value in data.values():
                self.data[self.exp_counter]['measurements'].append(value)
                self._add_to_table_noname(('measurements', [value]))
            return
        if 'black' in data.keys():
            if 'black' not in self.data.keys():
                self.data.update(data)
                self._add_to_table_noname(('black', [self.data['black']]))

    def _add_to_table_noname(self, data: tuple):
        """
        :param data in format {ethalon:[result]} or {measurements:[results]}:
        :return:
        """
        if data[0] == 'ethalon':
            self.setItem(self.counter - 1, 0, QTableWidgetItem(f'EC_{self.exp_counter}'))
            self.fill_table(data[1])
            return
        if data[0] == 'measurements':
            experiment_number = len(self.data[self.exp_counter]["measurements"])
            for measurement in data[1]:
                self.setItem(self.counter - 1, 0, QTableWidgetItem(f'Meas{experiment_number}'))
                self.fill_table(measurement)
            return
        if data[0] == 'measurements_single':
            for measurement in data[1]:
                self.setItem(self.counter - 1, 0, QTableWidgetItem(f'Meas_value'))
                self.fill_table(measurement)
            return
        if data[0] == 'black':
            for measurement in data[1]:
                self.setItem(self.counter - 1, 0, QTableWidgetItem('black'))
                self.fill_table(measurement)
        if data[0] == 'EC_correction_1':
            for measurement in data[1]:
                self.setItem(self.counter - 1, 0, QTableWidgetItem('EC_corr'))
                self.fill_table(measurement)
        if 'corr_exp' in data[0]:
            for measurement in data[1]:
                self.setItem(self.counter - 1, 0, QTableWidgetItem(data[0]))
                self.fill_table(measurement)

    def fill_table(self, measurement):
        for index, value in enumerate(measurement):
            self.setItem(self.counter - 1, index + 1, QTableWidgetItem(str(value)))
        self.counter += 1
        self.setRowCount(self.counter)


class MyTableMain(MyTableSetting):

    def __init__(self):
        super().__init__(size=(19, 1))
        self.ec1_corrected_data = {}
        self.ec2_corrected_data = {}

    def add(self, data: list):
        """
        Метод позволяет добавить данные в таблицу
        используя те данные, которые приходят нам с прибора

        :param data => результат который мы получили
                       с сенсора внутри спектрофотометра:
        :return:
        """
        type = data[0]
        value = data[1:]
        self._add_to_dict(data={type: value})

    def ec_correction_1(self):
        """
        Для работы метода необходимо чтобы
        в переменной self.data были сохранены хотябы:
            ethalon -> измерение при RGB(255, 255, 255)
            measurements -> обычное измерение для всего спектра
            black -> измерение при RGB(0, 0, 0)
         значений ethalon и measurements может быть несколько
        :return:
        """
        amount_of_ethalon = len(self.data)
        self.data.update({'EC_correction_1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]})
        # Find median of ethalonic measurement
        for experiment in self.data:
            if experiment not in self.SETTINGS.TECHNICAL_NAMES:
                for index, et_data in enumerate(self.data[experiment]['ethalon']):
                    self.data['EC_correction_1'][index] += round(et_data / amount_of_ethalon, 2)
        self._add_to_table_noname(('EC_correction_1', [self.data['EC_correction_1']]))
        # Correct value of each experiment according to average ethalonic measurement
        for experiment in self.data:
            self.ec1_corrected_data.update({experiment: []})
            if experiment not in self.SETTINGS.TECHNICAL_NAMES:
                for measure_data in self.data[experiment]['measurements']:
                    new_data = [
                        fabs(
                            round(value - self.data[experiment]['ethalon'][index] + self.data['EC_correction_1'][index],
                                  3))
                        for index, value in enumerate(measure_data)]
                    self.ec1_corrected_data[experiment].append(new_data)
                    self._add_to_table_noname(data=(f'ec1_corr_exp{experiment}', [new_data]))

    def ec_correction_2(self):
        from math import log10
        try:
            black = self.data['black']
        except KeyError:
            msg = QErrorMessage()
            msg.showMessage('You dont have measurement in black color ')
            msg.exec()
            return
        else:
            ec_corrected = self.data['EC_correction_1']
            # Start calculation process
            for experiment in self.data:
                self.ec2_corrected_data.update({experiment: []})
                if experiment not in self.SETTINGS.TECHNICAL_NAMES:
                    for measured_data in self.ec1_corrected_data[experiment]:
                        corrected_measurement_dat = []
                        for index, value in enumerate(measured_data):
                            i_black = black[index]
                            i_ref = ec_corrected[index]
                            i_sample = value
                            number = fabs((i_ref - i_black) / (i_sample - i_black))
                            corrected_result = round(log10(number), 2)
                            corrected_measurement_dat.append(corrected_result)
                        self.ec2_corrected_data[experiment].append(corrected_measurement_dat)
                        self._add_to_table_noname(data=(f'ec2_corr_exp{experiment}', [corrected_measurement_dat]))


if __name__ == '__main__':
    # et1 = ['ethalon', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    # m1 = ['measurements', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # m2 = ['measurements', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # m3 = ['measurements', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # et2 = ['ethalon', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # m4 = ['measurements', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # m5 = ['measurements', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # m6 = ['measurements', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # et3 = ['ethalon', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    # m7 = ['measurements', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # m8 = ['measurements', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # m9 = ['measurements', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # m10 = ['measurements', 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # datas = [et1, m1, m2, m3, et2, m4, m5, m6, et3, m7, m8, m9, m10]
    app = QApplication(sys.argv)
    widget = MyTableMain()
    widget.show()
    # widget.ec_correction_1()
    # widget.EC_correction_2()
    app.exec()
