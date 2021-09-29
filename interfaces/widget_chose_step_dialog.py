from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication

try:
    from dialog_chose_step import Ui_Dialog
except ModuleNotFoundError:
    from .dialog_chose_step import Ui_Dialog


class ChoseStepDialog(QDialog):

    def __init__(self):
        super(ChoseStepDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.__setup()
        self.is_modified = False
        self.__v = self.ui.vSpinBox.value()
        self.__h = self.ui.hSpinBox.value()
        self.__s = self.ui.sSpinBox.value()

    def __setup(self):
        self.ui.hSpinBox.setMaximum(60)
        self.ui.hSpinBox.setValue(1)
        self.ui.sSpinBox.setReadOnly(True)
        self.ui.sSpinBox.setMaximum(255)
        self.ui.sSpinBox.setValue(255)
        self.ui.vSpinBox.setReadOnly(True)
        self.ui.vSpinBox.setMaximum(255)
        self.ui.vSpinBox.setValue(255)
        self.ui.isModifyCB.stateChanged.connect(self.__change_mode)
        self.ui.sSpinBox.valueChanged.connect(self.set_s)
        self.ui.hSpinBox.valueChanged.connect(self.set_h)
        self.ui.vSpinBox.valueChanged.connect(self.set_v)

    def __change_mode(self, value):
        state = 0 if value else 1
        self.ui.vSpinBox.setReadOnly(state)
        self.ui.sSpinBox.setReadOnly(state)

    def get_hsv(self):
        return self.__h, self.__s, self.__v

    def get_s(self):
        return self.__s

    def get_v(self):
        return self.__v

    def get_h(self):
        return self.__h

    def set_h(self, value):
        self.__h = value

    def set_s(self, value):
        self.is_modified = True
        self.__s = value

    def set_v(self, value):
        self.is_modified = True
        self.__v = value


if __name__ == '__main__':
    app = QApplication([])
    widget = ChoseStepDialog()
    widget.show()
    app.exec()
