from django.db import connections

from projeto.models import Suppliers, PurchasingOrders

class PurchasingOrdersRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_PurchasingOrders")
        dataPurchasingOrders = self.cursor.fetchall()
        components_total = 0

        data = []

        data = [
            PurchasingOrders(
                id_purchasing_order=row[0],
                supplier=Suppliers(
                    name=row[10],
                    email=row[11],
                    nif=row[12],
                    phone=row[13],
                    address=row[14],
                    locality=row[15],
                    postal_code=row[16]
                ),
                #user=row[2],
                total_base=row[3],
                vat_total=row[4],
                discount_total=row[5],
                total=row[6],
                obs=row[7],
                delivery_date=row[8],
                created_at=row[9],
                #components_total=components_total
            ) for row in dataPurchasingOrders
        ]

        print(data)
        return data