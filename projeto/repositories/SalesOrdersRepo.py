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
                user=(
                    AuthUser(
                        id=row[1],
                        username=row[9],
                    )
                ),
                id_client_invoice=row[2],
                obs=row[3],
                total_base=row[4],
                vat_total=row[5],
                discount_total=row[6],
                total=row[7],
                created_at=row[8],
            ) for row in data
        ]
