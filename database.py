from sqlite3 import connect
import pandas as pd


class Database:
    def __init__(self):
        """
        Инициализация базы данных
        """
        self.conn = connect('journal.db')
        cursor = self.conn.cursor()
        self.conn.commit()
        cursor.close()

    def fill_db(self):
        """
        Заполнение БД данными из Excel
        :return:
        """
        journal = pd.read_excel('excel/journal2.xlsx', sheet_name=None)
        for sheet in journal:
            journal[sheet].to_sql(sheet, self.conn, index=False)
        self.conn.commit()

    def auth(self):
        """
        Авторизация
        :return:
        """
        cursor = self.conn.cursor()
        select = [str(i)[2:-3] for i in cursor.execute("SELECT login FROM authorization")]
        self.conn.commit()
        cursor.close()
        return select

    def log(self, login):
        """
        Загрузка данных об определенном студенте на основе введенного логина
        :param login: логин пользователя
        :return:
        """
        user = []
        cursor = self.conn.cursor()
        password = cursor.execute(f"SELECT password FROM authorization WHERE login = ('{login}')").fetchone()
        user.append(password)
        name = cursor.execute(f"SELECT id_student FROM Student WHERE surname = ('{login}')").fetchone()
        user.append(name)
        name = cursor.execute(f"SELECT name FROM Student WHERE surname = ('{login}')").fetchone()
        user.append(name)
        surname = cursor.execute(f"SELECT surname FROM Student WHERE surname = ('{login}')").fetchone()
        user.append(surname)
        self.conn.commit()
        cursor.close()
        return user

    def load_student(self, id):
        """
        Загрузка оценок студента по каждому предмету
        :param id: id студента
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT mark, id_subject FROM marks WHERE id_student = ('{id}')")
        marks = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return marks

    def subjects(self):
        """
        Загрузка всех предметов
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT subject_name FROM Subject")
        subjects = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return subjects

    def students(self):
        """
        Загрузка всех студентов из базы
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT id_student, name, surname FROM Student")
        students = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return students

    def update(self, id_student, marks, old):
        """
        Обновление оценки студента за предмет
        :param id_student: id студента
        :param marks: оценка
        :param old: старая оценка
        :return:
        """
        cursor = self.conn.cursor()
        id_st = int(id_student)
        marks_load = marks
        print(marks_load)
        for j in old:
            cursor.execute(f"DELETE FROM marks WHERE id_student = ('{id_st}')")
            self.conn.commit()
        for i in marks_load:
            mark = i[0]
            mark = int(mark)
            subject = i[1]
            subject = int(subject)
            cursor.execute(f"INSERT INTO marks (id_student, id_subject, mark) VALUES ('{id_st}','{subject}','{mark}')")
        self.conn.commit()
        cursor.close()
