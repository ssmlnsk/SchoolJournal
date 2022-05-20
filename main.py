from database import Database


class Split:
    def __init__(self):
        self.db = Database()

    def split(self, id):
        loaded = self.db.loadStudent(id)
        result = []
        res = []
        for i in loaded:
            try:
                mark = i[0]
                subject = i[1]
                result.append(mark)
                result.append(subject)
                res.append(result.copy())
                result.clear()
            except ValueError:
                continue

        return res
