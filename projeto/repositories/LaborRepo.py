from django.db import connections

from projeto.models import Labors


class LaborRepo:
    def __init__(self):
        self.cursor = connections['default'].cursor()

    def create(self, title, cost):
        self.cursor.execute(f"Call pa_create_labor('{title}', '{cost}')")
        #self.cursor.callproc("pa_create_labor", [title, cost])

    def find_all(self):
        self.cursor.execute(f"SELECT * FROM V_Labors")
        #self.cursor.callproc('V_Labors')
        data = self.cursor.fetchall()

        return [
            Labors(
                id_labor=labor[0],
                title=labor[1],
                cost=labor[2]
            ) for labor in data
        ]