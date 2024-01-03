from django.db import connections

from projeto.models import Labors


class LaborRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def create(self, title, cost):
        self.cursor.execute(f"Call PA_Create_Labor(%s, %s::MONEY)", [title, cost])

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