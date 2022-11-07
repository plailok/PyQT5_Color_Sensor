
class MyTableMain(MyTableSetting):
    class Exceller:

        def _file_dialog(self, type_of_dialog: int):
            if type_of_dialog == 1:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                files, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "output.xlsx",
                                                       options=options)
                return files
            if type_of_dialog == 2:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                        "Excel Files (*.xlsx,*xls);All Files (*)", options=options)
                return files

        def fill_table(self, measurement):
            for index, value in enumerate(measurement):
                self.setItem(self.counter - 1, index + 1, QTableWidgetItem(str(value)))
            self.counter += 1
            self.setRowCount(self.counter)

        def save_excel_file(self, data):
            try:
                file = self._file_dialog(1)
            except Exception as exc:
                print(exc)
                return
            data = self.get_all_table_result()
            indexes = [name.pop(0) for name in data]
            column = ['410 nm', '435 nm', '460 nm', '485 nm', '510 nm', '535 nm',
                      '560 nm', '585 nm', '610 nm', '645 nm', '680 nm', '705 nm',
                      '730 nm', '760 nm', '810 nm', '860 nm', '900 nm', '940 nm']
            d = pd.DataFrame(data, columns=column, index=indexes)
            d.to_excel(file, sheet_name='Result')

        def load_excel_file(self):
            """
            Import data from excel to our table.
            Now it's work in a way that
            :return:
            """
            try:
                file = self._file_dialog(2)
            except Exception as exc:
                print(exc)
                return
            data = pd.read_excel(file.pop()).values  # type(data) == np.array
            for row in data:
                self.add(data=row)

    def __init__(self):
        super().__init__(size=(19, 1))
        self.ec1_corrected_data = {}
        self.ec2_corrected_data = {}
        self.wb = None
        self.ws = None

    def add(self, data: list, wavelength: [float, str] = None):
        """
        Метод позволяет добавить данные в таблицу
        используя те данные, которые приходят нам с прибора

        :type wavelength: float, str
        :param wavelength: None
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
        for name in self.SETTINGS.TECHNICAL_NAMES:
            if name in self.data.keys():
                amount_of_ethalon -= 1
        self.data.update({'EC_correction_1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]})
        # Find median of references measurement
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
                            try:
                                number = fabs((i_sample - i_black) / (i_ref - i_black))
                            except ZeroDivisionError as error:
                                print(error)
                                print('Sample value', i_ref)
                                print('Black_value', i_black)
                                print('Corrected Sample Value', i_sample)
                                number = 0
                            try:
                                corrected_result = round(log10(number), 2)
                            except ValueError:
                                corrected_result = 'None'
                            corrected_measurement_dat.append(corrected_result)
                        self.ec2_corrected_data[experiment].append(corrected_measurement_dat)
                        self._add_to_table_noname(data=(f'ec2_corr_exp{experiment}', [corrected_measurement_dat]))

    def clear_table(self):
        """
        Clear all data in the table
        set experiment counter to 0
        set counter of row to 1
        set row count to 1
        """
        self.clear()
        self.exp_counter = 0
        self.counter = 1

        self.setRowCount(self.counter)
        self.setHorizontalHeaderLabels(self.SETTINGS.HEADER)

    def get_all_table_result(self) -> list:
        """
        Get data from the table
        Return data in format list['sample_name', values x 18 times]
        :return: list
        """
        data = []
        for i in range(self.rowCount() - 1):
            data.append([])
            for j in range(self.columnCount()):
                data[i].append(self.item(i, j).text())
        return data

