from database import Database
from main import Split
import logging

logging.basicConfig(level=logging.INFO)


class Facade:
    """
    Класс Фасада
    """
    def __init__(self):
        """
        Объявление класса базы данных и таблицы
        """
        self.db = Database()
        self.s = Split()
        # self.db.fill_db()

    def update(self):
        """
        Функция, осуществляющая вызов функции обновления таблицы
        :return:
        """
        self.db.update()
        logging.log(logging.INFO, 'facade: update')

    def load_student(self, id):
        """
        Функция, отвечающая за вызов функции загрузки формы для студента
        :param id: id студента
        :return:
        """
        data = self.s.split(id)
        logging.log(logging.INFO, 'facade: load')
        return data

    def load_teacher(self, id):
        """
        Функция, отвечающая за вызов функции загрузки формы для преподавателя
        :param id: id студента
        :return:
        """
        data = self.s.split(id)
        logging.log(logging.INFO, 'facade: load')
        return data

    def auth(self):
        """
        Функция авторизации
        :return:
        """
        users = self.db.auth()
        logging.log(logging.INFO, 'facade: auth')
        return users

    def log(self, login):
        """
        Загрузка данных о пользователе на основе введенного логина
        :param login: логин пользователя
        :return:
        """
        user = self.db.log(login)
        logging.log(logging.INFO, 'facade: log')
        return user

    def subjects(self):
        """
        Загрузка всех предметов
        :return:
        """
        subject = []
        temp = self.db.subjects()
        for i in temp:
            subject.append(i[0])
        logging.log(logging.INFO, 'facade: subjects')
        return subject

    def students(self):
        """
        Загрузка данных о студентах
        :return:
        """
        students = []
        student = []
        temp = self.db.students()
        for i in temp:
            student.append(str(i[0]))
            student.append(str(i[1]))
            student.append(str(i[2]))
            students.append(student.copy())
            student.clear()
        logging.log(logging.INFO, 'facade: students')
        return students

    def save(self, id, marks, old_marks):
        """
        Сохранение изменных данных об оценках и предметах
        :param id: id студента
        :param marks: новая оценка
        :param old_marks: старая оценка
        :return:
        """
        self.db.update(id, marks, old_marks)
        logging.log(logging.INFO, 'facade: save')
