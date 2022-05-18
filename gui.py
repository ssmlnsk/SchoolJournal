import sys
import logging

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from facade import Facade

logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self, facade):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('forms/authorization.ui', self)
        self.facade = facade
        self.user = []
        self.btnLogin.clicked.connect(lambda: self.login())
        logging.log(logging.INFO, 'Приложение запущено')

    def login(self):
        users = self.facade.auth()
        login = self.loginText.text()
        password = self.passwordText.text()
        if login != users[0]:
            password_current = self.facade.log(login)
            print(type(password_current))
            for i in password_current:
                print(i)
            if password != password_current[0]:
                name = password_current[1]
                surname = password_current[2]
                self.user = self.facade.loadStudent(name, surname)
                self.ui.hide()
                self.ui = StudentWidget(self.facade, self)
                self.ui.show()
                logging.log(logging.INFO, 'Открыто окно "Ученик"')
        else:
            password_current = self.facade.log(login)
            if password != password_current:
                self.ui.hide()
                self.ui = TeacherWidget(self.facade, self)
                self.ui.show()
                logging.log(logging.INFO, 'Открыто окно "Учитель"')


class StudentWidget(QtWidgets.QWidget):
    def __init__(self, facade, link=None):
        self.facade = facade
        self.link = link
        super(StudentWidget, self).__init__()
        self.ui = uic.loadUi('forms/studentWidget.ui', self)
        self.build()

    def build(self):

        counter = 0
        for i in self.link.user:
            self.tableWidget.setColumnCount(counter + 1)
            self.tableWidget.setItem(0, counter, QTableWidgetItem(str(i)))
            counter += 1


class TeacherWidget(QtWidgets.QWidget):
    def __init__(self, facade, link=None):
        self.facade = facade
        self.link = link
        super(TeacherWidget, self).__init__()
        self.ui = uic.loadUi('forms/teacherWidget.ui', self)
    #     self.build()
    #
    # def build(self):
    #     result = self.facade.loadTeacher()
    #     counter = 0
    #     for i in result:
    #         self.tableWidget.setColumnCount(counter + 1)
    #         self.tableWidget.setItem(0, counter, QTableWidgetItem(str(i)))
    #         counter += 1



class Builder:
    """
    Паттерн строитель.
    Это порождающий паттерн проектирования, который позволяет создавать сложные объекты пошагово.
    """

    def __init__(self):
        """
        Объявление переменных facade и gui.
        """
        self.facade = None
        self.gui = None

    def create_facade(self):
        """
        Создание ссылки на объект фасада (Facade).
        :return: None
        """
        self.facade = Facade()

    def create_gui(self):
        """
        Создание ссылки на объект графики (MainWindow), если создана ссылка на фасад.
        :return: None
        """
        if self.facade is not None:
            self.gui = MainWindow(self.facade)

    def get_result(self):
        """
        Получение ссылки на объект графики (MainWindow).
        :return: gui - ссылка на объект графики.
        """
        if self.facade is not None and self.gui is not None:
            return self.gui


if __name__ == '__main__':
    qapp = QtWidgets.QApplication(sys.argv)
    builder = Builder()
    builder.create_facade()
    builder.create_gui()
    window = builder.get_result()
    window.show()
    qapp.exec()
