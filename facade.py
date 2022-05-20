from database import Database
from main import Split
import logging

logging.basicConfig(level=logging.INFO)


class Facade:
    def __init__(self):
        self.db = Database()
        self.s = Split()
        # self.db.fill_db()

    def update(self):
        self.db.update()
        logging.log(logging.INFO, 'facade: update')

    def loadStudent(self, id):
        data = self.s.split(id)
        logging.log(logging.INFO, 'facade: load')
        return data

    def loadTeacher(self, id):
        data = self.s.split(id)
        logging.log(logging.INFO, 'facade: load')
        return data

    def auth(self):
        users = self.db.auth()
        return users

    def log(self, login):
        user = self.db.log(login)
        return user

    def subjects(self):
        subject = []
        temp = self.db.subjects()
        for i in temp:
            subject.append(i[0])
        return subject

    def students(self):
        students = []
        student = []
        temp = self.db.students()
        for i in temp:
            student.append(str(i[0]))
            student.append(str(i[1]))
            student.append(str(i[2]))
            students.append(student.copy())
            student.clear()
        return students

    def save(self, name, surname, marks):
        self.db.update(name, surname, marks)

if __name__ == '__main__':
    facade = Facade()
    print(facade.subjects())
        