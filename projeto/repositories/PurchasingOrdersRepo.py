from django.db import connections

from projeto.models import Suppliers, PurchasingOrders, AuthUser


class PurchasingOrdersRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_PurchasingOrders")
        dataPurchasingOrders = self.cursor.fetchall()

        data = [
            PurchasingOrders(
                id_purchasing_order=row[0],
                supplier=Suppliers(
                    id_supplier=row[1],
                    name=row[2],
                ),
                user=AuthUser(
                    username=row[4],
                ),
                delivery_date=row[5],
                created_at=row[6],
                obs=row[7],
                total_base=row[8],
                vat_total=row[9],
                discount_total=row[10],
                total=row[11],
            ) for row in dataPurchasingOrders
        ]

        return data

    def create(self, id_supplier, id_user, delivery_date, obs, products=[]):
        self.cursor.callproc('FN_Create_PurchasingOrder', [id_supplier, id_user, delivery_date, obs])
        reponse = self.cursor.fetchone()

        print()

        if reponse[0]:
            id_purchasing_order = reponse[0]

            print(id_purchasing_order)

            for product in products:
                self.cursor.execute('Call PA_InsertLine_PurchasingOrder(%s, %s, %s, %s, %s, %s)', [
                    id_purchasing_order,
                    product["id"],
                    product["quantity"],
                    product["price_base"],
                    product["vat"] or 0,
                    product["discount"] or 0,
                ])

            return True
