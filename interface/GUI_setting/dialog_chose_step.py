# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\interface\dialog_chose_step.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(237, 106)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.mainHLayout = QtWidgets.QHBoxLayout()
        self.mainHLayout.setObjectName("mainHLayout")
        self.leftVLayout = QtWidgets.QVBoxLayout()
        self.leftVLayout.setObjectName("leftVLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hLable = QtWidgets.QLabel(Dialog)
        self.hLable.setObjectName("hLable")
        self.horizontalLayout.addWidget(self.hLable)
        self.hSpinBox = QtWidgets.QSpinBox(Dialog)
        self.hSpinBox.setObjectName("hSpinBox")
        self.horizontalLayout.addWidget(self.hSpinBox)
        self.leftVLayout.addLayout(self.horizontalLayout)
        self.isModifyCB = QtWidgets.QCheckBox(Dialog)
        self.isModifyCB.setObjectName("isModifyCB")
        self.leftVLayout.addWidget(self.isModifyCB)
        self.leftVLayout.setStretch(0, 1)
        self.leftVLayout.setStretch(1, 1)
        self.mainHLayout.addLayout(self.leftVLayout)
        self.rightVLayout = QtWidgets.QVBoxLayout()
        self.rightVLayout.setObjectName("rightVLayout")
        self.valueHLayout = QtWidgets.QHBoxLayout()
        self.valueHLayout.setObjectName("valueHLayout")
        self.vLable = QtWidgets.QLabel(Dialog)
        self.vLable.setTextFormat(QtCore.Qt.RichText)
        self.vLable.setAlignment(QtCore.Qt.AlignCenter)
        self.vLable.setObjectName("vLable")
        self.valueHLayout.addWidget(self.vLable)
        self.vSpinBox = QtWidgets.QSpinBox(Dialog)
        self.vSpinBox.setObjectName("vSpinBox")
        self.valueHLayout.addWidget(self.vSpinBox)
        self.rightVLayout.addLayout(self.valueHLayout)
        self.saturationHLayout = QtWidgets.QHBoxLayout()
        self.saturationHLayout.setObjectName("saturationHLayout")
        self.sLable = QtWidgets.QLabel(Dialog)
        self.sLable.setAlignment(QtCore.Qt.AlignCenter)
        self.sLable.setObjectName("sLable")
        self.saturationHLayout.addWidget(self.sLable)
        self.sSpinBox = QtWidgets.QSpinBox(Dialog)
        self.sSpinBox.setObjectName("sSpinBox")
        self.saturationHLayout.addWidget(self.sSpinBox)
        self.rightVLayout.addLayout(self.saturationHLayout)
        self.rightVLayout.setStretch(0, 1)
        self.rightVLayout.setStretch(1, 1)
        self.mainHLayout.addLayout(self.rightVLayout)
        self.verticalLayout_3.addLayout(self.mainHLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.hLable.setText(_translate("Dialog", "Step H:"))
        self.isModifyCB.setText(_translate("Dialog", "Modify V, S values"))
        self.vLable.setText(_translate("Dialog", "V"))
        self.sLable.setText(_translate("Dialog", "S"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
