# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    import sys
    from PyQt5 import QtWidgets
    from interfaces.main_window_settings import SensorMainWindowControl

    app = QtWidgets.QApplication([])
    application = SensorMainWindowControl()
    application.show()
    sys.exit(app.exec())

#TODO 1. Сохранение в Ексель
#TODO 2. Импорт из Ексель
#TODO 3. Заменить Коннект на Дисконнект (если есть коннект) Done
#TODO 4. Заменить инморт на Экспорт
#TODO 5. добавить кнопку Импорт
#TODO 6. По нажатию на "Мульти" выбор шага Done
#TODO 7. Добавить запись цвета куда либо (подумать куда?)
#TODO 8. Скомпелировать в экзешник




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
