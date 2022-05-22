from database import Database


class Split:
    def __init__(self):
        """
        Объявление класса базы данных
        """
        self.db = Database()

    def split(self, id):
        """
        я хз че это
        :param id: id студента (мб)
        :return:
        """
        loaded = self.db.load_student(id)
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
