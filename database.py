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
        journal = pd.read_excel('excel/journal.xlsx', sheet_name = None)
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
        name = cursor.execute(f"SELECT name FROM authorization WHERE login = ('{login}')").fetchone()
        user.append(name)
        surname = cursor.execute(f"SELECT surname FROM authorization WHERE login = ('{login}')").fetchone()
        user.append(surname)
        self.conn.commit()
        cursor.close()
        print(user)
        return user

    def loadStudent(self, name, surname):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT markMath FROM Math WHERE name = ('{name}') AND surname = ('{surname}')")
        math = cursor.fetchall()
        cursor.execute(f"SELECT markRussian FROM Russian WHERE name = ('{name}') AND surname = ('{surname}')")
        russian = cursor.fetchall()
        cursor.execute(f"SELECT markLiterature FROM Literature WHERE name = ('{name}') AND surname = ('{surname}')")
        literature = cursor.fetchall()
        result = [math, russian, literature]
        self.conn.commit()
        cursor.close()
        return result

    def loadTeacher(self, name, surname):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT markMath FROM Math WHERE name = ('{name}') AND surname = ('{surname}')")
        math = cursor.fetchall()
        cursor.execute(f"SELECT markRussian FROM Russian WHERE name = ('{name}') AND surname = ('{surname}')")
        russian = cursor.fetchall()
        cursor.execute(f"SELECT markLiterature FROM Literature WHERE name = ('{name}') AND surname = ('{surname}')")
        literature = cursor.fetchall()
        student = [math, russian, literature]
        self.conn.commit()
        cursor.close()
        return student

    def update(self):
        pass


if __name__ == '__main__':
    db = Database()
    db.log('Petrov')