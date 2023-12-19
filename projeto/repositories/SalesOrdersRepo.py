from django.db import connections

from projeto.models import SalesOrders, AuthUser


class SalesOrdersRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute('SELECT * FROM V_SalesOrders')

        data = self.cursor.fetchall()

        return [
            SalesOrders(
                id_sale_order=row[0],
                user=AuthUser(
                        id=row[1],
                        username=row[2],
                    ),
                obs=row[5],
                total_base=row[6],
                created_at=row[4],
            ) for row in data
        ]
