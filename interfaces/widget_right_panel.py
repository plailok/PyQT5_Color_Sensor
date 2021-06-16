import csv
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget, QTableWidgetItem, QFileDialog

from right_panel import Ui_Form as WidgetRightPanel


class RightPanel(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent if parent else None
        self.ui = WidgetRightPanel()
        self.ui.setupUi(self)
        self.count = 0
        self.file_to_save_name = None
        self.admin_widget = None
        self.isSaved = False
        self.LABELS = ['SAMPLE',
                       'λ1', 'λ2', 'λ3', 'λ4', 'λ5', 'λ6',
                       'λ7', 'λ8', 'λ9', 'λ10', 'λ11', 'λ12',
                       'λ13', 'λ14', 'λ15', 'λ16', 'λ17', 'λ18']
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setHorizontalHeaderLabels(self.LABELS)
        self.ui.isAdminModeCheckButton.stateChanged.connect(self.__isAdminMode)
        self.ui.saveTableButton.clicked.connect(self.save_table)
        self.ui.clearTableButton.clicked.connect(self.clear_table)

    def save_table(self):
        if not self.isSaved:
            if not self.file_to_save_name:
                self.file_to_save_name = QFileDialog.getSaveFileName(self, 'Chose .csv', filter="Table File csv (*.csv)")
            result_to_save = []
            for line in range(self.count):
                result_to_save = []
                for item in range(len(self.LABELS)):
                    current_cell = self.ui.tableWidget.item(line, item)
                    if item == 0:
                        name = current_cell.text() if current_cell is not None else '-'
                        result_to_save.append(name)
                    else:
                        result_to_save.append(current_cell.text())

                with open(self.file_to_save_name[0], 'a+') as f:
                    file_writer = csv.writer(f)
                    file_writer.writerow(result_to_save)

    def clear_table(self):
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setHorizontalHeaderLabels(self.LABELS)

    def admin_widget_control(self, isHide: int):
        self.admin_widget.hide() if isHide == 0 else self.admin_widget.show()

    def __isAdminMode(self, value: int):
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

    def set_one_value(self, col, value: str):
        pass

    def set_list_value(self, values: list):
        for index, value in enumerate(values):
            if value == 'None':
                continue
            else:
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(self.count, index, item)
        self.increase_counter()
        self.isSaved = False

    def increase_counter(self):
        self.count += 1
        self.ui.tableWidget.setRowCount(self.count + 1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = RightPanel()
    application.show()
    test = ['Name1', '123', '234', '123', '234', '123', '234',
            '123', '234', '123', '234', '123', '234',
            '123', '234', '123', '234', '123', '234']
    application.set_list_value(test)
    test = ['None', '123', '234', '123', '234', '123', '234',
            '123', '234', '123', '234', '123', '234',
            '123', '234', '123', '234', '123', '234']
    application.set_list_value(test)
    application.set_list_value(test)
    test = ['Name2', '123', '234', '123', '234', '123', '234',
            '123', '234', '123', '234', '123', '234',
            '123', '234', '123', '234', '123', '234']
    application.set_list_value(test)
    sys.exit(app.exec())
