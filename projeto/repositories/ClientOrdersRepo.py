from django.db import connections

from projeto.models import ClientOrders, Clients


class ClientOrdersRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_ClientOrders")
        data = self.cursor.fetchall()

        return [ClientOrders(
            id_client_order=row[0],
            client=(Clients(
                id_client=row[1],
                name=row[9],
            )),
            id_sale_order=row[2],
            total_base=row[3],
            vat_total=row[4],
            discount_total=row[5],
            total=row[6],
            created_at=row[8],
        ) for row in data]
