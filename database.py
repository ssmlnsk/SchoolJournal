from sqlite3 import connect
import pandas as pd
import json


class Database:
    def __init__(self):
        self.conn = connect('journal.db')
        cursor = self.conn.cursor()
        # cursor.execute("CREATE TABLE IF NOT EXISTS authorization (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT, "
        #                "password TEXT)")
        # cursor.execute("CREATE TABLE IF NOT EXISTS Math (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, "
        #                "surname TEXT, markMath INTEGER)")
        # cursor.execute("CREATE TABLE IF NOT EXISTS Russian (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, "
        #                "surname TEXT, markRussian INTEGER)")
        # cursor.execute("CREATE TABLE IF NOT EXISTS Literature (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, "
        #                "surname TEXT, markLiterature INTEGER)")
        self.conn.commit()
        cursor.close()

    def fill_db(self):
        journal = pd.read_excel('excel/journal2.xlsx', sheet_name = None)
        for sheet in journal:
            journal[sheet].to_sql(sheet, self.conn, index=False)
        self.conn.commit()

    def auth(self):
        cursor = self.conn.cursor()
        select = [str(i)[2:-3] for i in cursor.execute("SELECT login FROM authorization")]
        self.conn.commit()
        cursor.close()
        return select

    def log(self, login):
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

    def loadStudent(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT mark, id_subject FROM marks WHERE id_student = ('{id}')")
        marks = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return marks

    def subjects(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT subject_name FROM Subject")
        subjects = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return subjects

    def loadTeacher(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT mark, id_subject FROM marks WHERE id_student = ('{id}')")
        marks = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return marks

    def students(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT id_student, name, surname FROM Student")
        students = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return students

    def update(self, name, surname, marks):
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE Math SET markMath = ('{marks[0]}') WHERE name = ('{name}') AND surname = ('{surname}');")
        cursor.execute(f"UPDATE Russian SET markRussian = ('{marks[1]}') WHERE name = ('{name}') AND surname = ('{surname}');")
        cursor.execute(f"UPDATE Literature SET markLiterature = ('{marks[2]}') WHERE name = ('{name}') AND surname = ('{surname}');")
        self.conn.commit()
        cursor.close()


if __name__ == '__main__':
    db = Database()
    print(db.subjects())
