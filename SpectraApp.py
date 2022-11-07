# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    import sys
    from PyQt5 import QtWidgets
    from interface.main_window_control import SensorMainWindowControl

    app = QtWidgets.QApplication([])
    application = SensorMainWindowControl()
    application.show()
    sys.exit(app.exec())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
