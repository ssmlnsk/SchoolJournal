import sys
import logging

from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from facade import Facade

logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self, facade):
        """
        Инициализация формы авторизации
        :param facade: facade
        """
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('forms/authorization.ui', self)
        self.facade = facade
        self.user = []
        self.btnLogin.clicked.connect(lambda: self.login())
        logging.log(logging.INFO, 'Приложение запущено')

    def login(self):
        """
        Авторизация пользователя
        :return:
        """
        self.user = []
        users = self.facade.auth()
        login = self.loginText.text()
        password = self.passwordText.text()
        if bool(login in users) == False:
            self.warning_login()
        else:
            if login != users[0]:
                log = self.facade.log(login)
                password_current = []
                for i in log:
                    password_current.append(str(i[0]))
                if password == password_current[0]:
                    id_student = password_current[1]
                    self.user = self.facade.load_student(id_student)
                    self.ui.hide()
                    self.ui = StudentWidget(self.facade, self)
                    self.ui.show()
                    logging.log(logging.INFO, 'Открыто окно "Ученик"')
                else:
                    self.warning_password()
            else:
                log = self.facade.log(login)
                password_current = log[0]
                if password == password_current[0]:
                    self.ui.hide()
                    self.ui = TeacherWidget(self.facade, self)
                    self.ui.show()
                    logging.log(logging.INFO, 'Открыто окно "Учитель"')
                else:
                    self.warning_password()

    def warning_login(self):
        """
        Создание MessageBox, если данные содержат буквы и символы.
        :return: None
        """
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle("Ошибка ввода")
        messagebox.setText("Неверный логин!")
        messagebox.setIcon(QMessageBox.Warning)
        messagebox.setStandardButtons(QMessageBox.Ok)

        messagebox.show()
        logging.log(logging.INFO, 'Открыто диалоговое окно "Ошибка ввода"')

    def warning_password(self):
        """
        Создание MessageBox, если данные содержат буквы и символы.
        :return: None
        """
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle("Ошибка ввода")
        messagebox.setText("Неверный пароль!")
        messagebox.setIcon(QMessageBox.Warning)
        messagebox.setStandardButtons(QMessageBox.Ok)

        messagebox.show()
        logging.log(logging.INFO, 'Открыто диалоговое окно "Ошибка ввода"')


class StudentWidget(QtWidgets.QWidget):
    """
    Режим работы приложения для студента
    :param:
    """

    def __init__(self, facade, link=None):
        """
        Инициализация
        :param facade: facade
        :param link: link
        """
        self.facade = facade
        self.link = link
        super(StudentWidget, self).__init__()
        self.ui = uic.loadUi('forms/studentWidget.ui', self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        self.subjects = self.facade.subjects()
        self.build()

    def build(self):
        """
        Заполнение таблицы строками, столбцами с добавлением в них элементов.
        :return:
        """
        self.tableWidget.setHorizontalHeaderLabels(['Mark', 'Subject'])
        counter = 0
        for x, i in enumerate(self.link.user):
            mark = i[0]
            subject = i[1]
            count = 1
            item = QTableWidgetItem()
            item.setText(str(mark))
            self.tableWidget.setRowCount(counter + 1)
            self.tableWidget.setItem(counter, 0, item)
            if mark == 5:
                item.setBackground(QtGui.QColor(188, 245, 188))
            if mark == 4:
                item.setBackground(QtGui.QColor(255, 255, 173))
            if mark == 3:
                item.setBackground(QtGui.QColor(255, 221, 199))
            if mark == 2:
                item.setBackground(QtGui.QColor(255, 167, 153))
            logging.log(logging.INFO, 'Добавлена оценка')
            for s in self.subjects:
                if count == subject:
                    item2 = QTableWidgetItem()
                    item2.setText(str(s))
                    self.tableWidget.setRowCount(counter + 1)
                    self.tableWidget.setItem(counter, 1, item2)
                    counter += 1
                    logging.log(logging.INFO, 'Добавлен предмет')
                    logging.log(logging.INFO, 'Добавлена строка')
                    break
                else:
                    count += 1


class TeacherWidget(QtWidgets.QWidget):

    """
    Режим работы приложения для преподавателя
    """

    def __init__(self, facade, link=None):
        """
        Инициализация формы
        :param facade: facade
        :param link: link
        """
        self.facade = facade
        self.link = link
        self.index = 0
        super(TeacherWidget, self).__init__()
        self.ui = uic.loadUi('forms/teacherWidget.ui', self)
        self.btnNext.clicked.connect(lambda: self.button_next())
        self.btnPrev.clicked.connect(lambda: self.button_prev())
        self.btnAdd.clicked.connect(lambda: self.insert_row())
        self.btnSave.clicked.connect(self.save)
        self.tableWidget.setColumnCount(2)

        self.students = self.facade.students()
        self.subjects = self.facade.subjects()
        self.build(0)

    def build(self, index):
        """
        Заполнение таблицы строками, столбцами с добавлением в них элементов.
        :return:
        """
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['Mark', 'Subject'])
        student = self.students[index]
        self.id_student = student[0]
        self.name = student[1]
        self.surname = student[2]
        self.student_name.setText(f"{self.name} {self.surname}")
        marks = self.facade.load_teacher(self.id_student)
        counter = 0
        for x, i in enumerate(marks):
            self.mark = i[0]
            self.subject = i[1]
            count = 1
            item = QTableWidgetItem()
            item.setText(str(self.mark))
            self.tableWidget.setRowCount(counter + 1)
            self.tableWidget.setItem(counter, 0, item)
            logging.log(logging.INFO, 'Добавлена оценка')
            for s in self.subjects:
                if count == self.subject:
                    item2 = QTableWidgetItem()
                    item2.setText(str(s))
                    self.tableWidget.setRowCount(counter + 1)
                    self.tableWidget.setItem(counter, 1, item2)
                    logging.log(logging.INFO, 'Добавлен предмет')
                    logging.log(logging.INFO, 'Добавлена строка')
                    counter += 1
                    break
                else:
                    count += 1

    def button_next(self):
        """
        Переход на таблицу с оценками следующего студента
        :return:
        """
        if self.index < len(self.students) - 1:
            self.index += 1
            self.build(self.index)
            logging.log(logging.INFO, 'Следующий учащийся')
        else:
            print('Ты чего?')

    def button_prev(self):
        """
        Переход на таблицу с оценками предыдущего студента
        :return:
        """
        if self.index > 0:
            self.index -= 1
            self.build(self.index)
            logging.log(logging.INFO, 'Предыдущий учащийся')
        else:
            print('Ты че, дурачок?')

    def save(self):
        """
        Сохранение оценок
        :return:
        """
        old_marks = self.facade.load_student(self.id_student)
        print(old_marks)
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        marks = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                try:
                    tmp.append(self.tableWidget.item(row, col).text())
                except:
                    tmp.append('No data')
            marks.append(tmp)

        save_marks = []
        for i in marks:
            default = ['2', '3', '4', '5']
            save_mark = []
            mark = i[0]
            if bool(mark in default) == False:
                self.warning_no_default()
                break
            else:
                subject = i[1]
                counter = 1
                save_mark.append(int(mark))
                if bool(subject in self.subjects) == False:
                    self.warning_no_subject()
                else:
                    for s in self.subjects:
                        if subject == s:
                            subject = counter
                            save_mark.append(subject)
                            counter += 1
                            break
                        else:
                            counter += 1
                    save_marks.append(save_mark.copy())

        self.facade.save(self.id_student, save_marks, old_marks)
        logging.log(logging.INFO, 'Данные сохранены')

    def insert_row(self):
        """
        Добавление новой строки для предмета и оценки по нему
        :return:
        """
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        logging.log(logging.INFO, 'Добавлена строка')

    def warning_no_default(self):
        """
        Предупреждение об ошибке ввода — введенное число не входит в диапазон оценок (2, 3, 4, 5)
        :return:
        """
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle("Ошибка ввода")
        messagebox.setText("Оценка не равна оценкам:")
        messagebox.setInformativeText("2, 3, 4 ,5")
        messagebox.setIcon(QMessageBox.Warning)
        messagebox.setStandardButtons(QMessageBox.Ok)

        messagebox.show()
        logging.log(logging.INFO, 'Открыто диалоговое окно "Ошибка ввода"')

    def warning_no_subject(self):
        """
        Предупреждение об ошибке — введенный предмет отстутствует в базе данных
        :return:
        """
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle("Ошибка ввода")
        messagebox.setText("Данный предмет не имеется в базе")
        messagebox.setIcon(QMessageBox.Warning)
        messagebox.setStandardButtons(QMessageBox.Ok)

        messagebox.show()
        logging.log(logging.INFO, 'Открыто диалоговое окно "Ошибка ввода"')


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