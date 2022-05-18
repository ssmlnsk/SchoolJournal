from database import Database
from main import Split
import logging

logging.basicConfig(level=logging.INFO)


class Facade:
    def __init__(self):
        self.db = Database()
        self.s = Split()

    def update(self):
        self.db.update()
        logging.log(logging.INFO, 'facade: update')

    def loadStudent(self, name, surname):
        data = self.s.split(name, surname)
        print(data)
        logging.log(logging.INFO, 'facade: load')
        return data

    def loadTeacher(self, name, surname):
        data = self.s.split(name, surname)
        print(data)
        logging.log(logging.INFO, 'facade: load')
        return data

    def auth(self):
        users = self.db.auth()
        return users

    def log(self, login):
        user = self.db.log(login)
        print(user)
        return user
