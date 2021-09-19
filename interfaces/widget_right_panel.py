from datetime import datetime

import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget, QTableWidgetItem, QFileDialog

try:
    from right_panel import Ui_Form as WidgetRightPanel
    from widget_table import MyTableMain
except ModuleNotFoundError as exc:
    print(exc)
    from .right_panel import Ui_Form as WidgetRightPanel
    from .widget_table import MyTableMain

class ExcelSaver:
    class Default:
        NAME = f"{datetime.now()}_data_set"

    def __init__(self, name=None):
        self.result = {}
        self.labels = ['Name',
                       '410', '435', '460', '485', '510', '535',
                       '560', '585', '610', '645', '680', '705',
                       '730', '760', '810', '860', '900', '940']
        self.last_s = 'S0'
        self.current_set = 0
        self.file_name = name[0].url().split('/')[-1]

    def save(self):
        data = pd.DataFrame(self.result)
        data.to_excel(self.file_name, sheet_name='Set_1')

    def add(self, result_in_line: dict):
        """
        По логике функция ожидает следующий вариант результата
        result_in_line = ['Set_name', 'λ1', 'λ2', 'λ3', 'λ4', 'λ5',
                        'λ6','λ7', 'λ8', 'λ9', 'λ10', 'λ11', 'λ12',
                        'λ13', 'λ14', 'λ15', 'λ16', 'λ17', 'λ18']
        :param result_in_line:
        :return:
        """
        if isinstance(result_in_line, list):
            if result_in_line[0][0].lower() == 'e':
                self.result[result_in_line[0]] = {self.labels[index]: result_in_line[index] for index in
                                                  range(1, len(result_in_line))}
            elif result_in_line[0][0].lower() == 's' and self.result.get(result_in_line[0]) is None:
                self.result[result_in_line[0]] = {self.labels[index]: result_in_line[index] for index in
                                                  range(1, len(result_in_line))}
            else:
                self.current_set += 1
                new_name = f'S{self.current_set}'
                result_in_line[0] = new_name
                self.result[result_in_line[0]] = {self.labels[index]: result_in_line[index] for index in
                                                  range(1, len(result_in_line))}

    def load(self):
        pass


class RightPanel(QtWidgets.QWidget):
    REGULAR_EC = r'EC\d*'
    REGULAR_S = r'S\d*'

    def __init__(self, parent=None):
        """
        self.RESULT = {sample_count: {n:[result_list]}}
        self.RESULT[sample_count] = {n:[result_list]}
        self.RESULT[sample_count][n] = [result_list]
        :param parent:
        """
        super().__init__()
        self.parent = parent if parent else None
        self.ui = WidgetRightPanel()
        self.ui.setupUi(self)
        self.total_count = 0
        self.file_to_save_name = None
        self.admin_widget = None
        self.isSaved = False
        self.LABELS = ['Name',
                       '410', '435', '460', '485', '510', '535',
                       '560', '585', '610', '645', '680', '705',
                       '730', '760', '810', '860', '900', '940']
        self.RESULT = []
        self.saver = None
        self.__set_table()

    def set_list_value(self, values: list):
        self.RESULT.append(values)
        print(self.RESULT)
        for index, value in enumerate(values):
            if value == 'None':
                continue
            else:
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(self.total_count, index, item)
        self.increase_counter()
        self.isSaved = False

    def increase_counter(self):
        self.total_count += 1
        self.ui.tableWidget.setRowCount(self.total_count + 1)

    def admin_widget_control(self, is_hide: int):
        self.admin_widget.hide() if is_hide == 0 else self.admin_widget.show()

    def __set_table(self):
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setHorizontalHeaderLabels(self.ui.tableWidget.SETTINGS.HEADER)
        self.ui.isAdminModeCheckButton.stateChanged.connect(self.__is_admin_mode)
        self.ui.saveTableButton.clicked.connect(self.__save_table)
        self.ui.clearTableButton.clicked.connect(self.__clear_table)

    def __save_table(self):
        if not self.saver:
            file_name = QFileDialog.getSaveFileUrl(caption="Open ExcelFile",
                                                   filter="Excel File (*.xlsx *.xls )")
            if not file_name:
                file_name = 'Default_table'
            self.saver = ExcelSaver(name=file_name)
        self.__add_to_saver()
        self.saver.save()

    def __clear_table(self):
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setHorizontalHeaderLabels(self.LABELS)
        self.total_count = 0
        self.ui.tableWidget.setRowCount(1)

    def __add_to_saver(self):
        for result in self.RESULT:
            self.saver.add(result)

    def __is_admin_mode(self, value: int):
        self.__add_admin_panel() if not self.admin_widget else self.admin_widget_control(value)

    def __add_admin_panel(self):
        self.admin_widget = QWidget()
        line = QLineEdit()
        line.setAlignment(Qt.AlignHCenter)
        line.setPlaceholderText("Input Command")
        button = QPushButton("Send Command")
        h_layout = QHBoxLayout()
        h_layout.addWidget(line, 2)
        h_layout.addWidget(button, 1)
        self.admin_widget.setLayout(h_layout)
        self.ui.verticalLayout_2.addWidget(self.admin_widget)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication([])
    application = RightPanel()
    application.show()
    # test = ['EC0', '23.21', '76.2', '61.2', '11', '23', '234',
    #         '12', '11.25', '97.3', '88', '54', '234',
    #         '23', '34.12', '54', '77', '12', '23']
    # application.set_list_value(test)
    # test = ['S1', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['EC1', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['S1', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['EC2', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['S1', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['EC3', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['S1', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['EC4', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['S1', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['EC5', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['S1', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['EC6', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['S1', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['EC7', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['S1', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['EC8', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    # test = ['S1', '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234',
    #         '123', '234', '123', '234', '123', '234']
    # application.set_list_value(test)
    sys.exit(app.exec())
