from database import Database


class Split:
    def __init__(self):
        self.db = Database()

    def split(self, name, surname):
        loaded = str(self.db.loadStudent(name, surname))
        result = []
        for i in loaded:
            try:
                num = int(i)
                result.append(num)
            except ValueError:
                continue
        return result
