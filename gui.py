import sys
import logging

from PyQt5 import uic, QtWidgets
from PyQt5.QtSql import QSqlTableModel
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
        self.user = []
        users = self.facade.auth()
        login = self.loginText.text()
        password = self.passwordText.text()
        if login != users[0]:
            log = self.facade.log(login)
            password_current = []
            for i in log:
                password_current.append(str(i[0]))
            if password == password_current[0]:
                name = password_current[1]
                surname = password_current[2]

                self.user = self.facade.loadStudent(id)
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
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(1)
        self.build()

    def build(self):
        self.tableWidget.setHorizontalHeaderLabels(['Mark', 'Subject'])
        for x, j in enumerate(self.link.user):
            item = QTableWidgetItem()
            item.setText(str(j))
            self.tableWidget.setItem(0, x, item)

        for x, i in enumerate(marks):
            mark = i[0]
            subject = i[1]
            count = 1
            item = QTableWidgetItem()
            item.setText(str(mark))
            self.tableWidget.setRowCount(counter + 1)
            self.tableWidget.setItem(counter, 0, item)
            for s in self.subjects:
                if count == subject:
                    item2 = QTableWidgetItem()
                    item2.setText(str(s))
                    self.tableWidget.setRowCount(counter + 1)
                    self.tableWidget.setItem(counter, 1, item2)
                    counter += 1
                    break
                else:
                    count += 1


class TeacherWidget(QtWidgets.QWidget):
    def __init__(self, facade, link=None):
        self.facade = facade
        self.link = link
        self.index = 0
        super(TeacherWidget, self).__init__()
        self.ui = uic.loadUi('forms/teacherWidget.ui', self)
        self.btnNext.clicked.connect(lambda: self.buttonNext())
        self.btnPrev.clicked.connect(lambda: self.buttonPrev())
        self.btnSave.clicked.connect(self.save)
        self.tableWidget.setColumnCount(2)
        
        self.students = self.facade.students()
        self.subjects = self.facade.subjects()
        self.UpdateTable(0)

    def UpdateTable(self, index):
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['Mark', 'Subject'])
        student = self.students[index]
        self.id_student = student[0]
        self.name = student[1]
        self.surname = student[2]
        self.student_name.setText(f"{self.name} {self.surname}")
        marks = self.facade.loadTeacher(self.id_student)
        counter = 0
        for x, i in enumerate(marks):
            mark = i[0]
            subject = i[1]
            count = 1
            item = QTableWidgetItem()
            item.setText(str(mark))
            self.tableWidget.setRowCount(counter + 1)
            self.tableWidget.setItem(counter, 0, item)
            for s in self.subjects:
                if count == subject:
                    item2 = QTableWidgetItem()
                    item2.setText(str(s))
                    self.tableWidget.setRowCount(counter + 1)
                    self.tableWidget.setItem(counter, 1, item2)
                    counter += 1
                    break
                else:
                    count += 1

    def buttonNext(self):
        if self.index < len(self.students) - 1:
            self.index += 1
            self.UpdateTable(self.index)
        else:
            print('Ты чего?')

    def save(self):
        name_s = self.name
        surname_s = self.surname
        marks = [self.tableWidget.item(0, 0).text(), self.tableWidget.item(0, 1).text(),
                 self.tableWidget.item(0, 2).text()]
        print([name_s, surname_s, marks])
        self.facade.save(name_s, surname_s, marks)

    def buttonPrev(self):
            if self.index > 0:
                self.index -= 1
                self.UpdateTable(self.index)
            else:
                print('Ты че, дурачок?')


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
