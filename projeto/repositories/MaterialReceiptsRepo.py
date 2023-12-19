from django.db import connections, models

from projeto.models import MaterialReceipts, Suppliers, AuthUser, PurchasingOrders


class MaterialReceiptsView(MaterialReceipts):
    supplier = models.ForeignKey('Suppliers', models.DO_NOTHING, db_column='id_supplier')

class MaterialReceiptsRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_MaterialReceipts")
        data = self.cursor.fetchall()

        return [
            MaterialReceiptsView(
                id_material_receipt=row[0],
                purchasing_order=PurchasingOrders(
                    id_purchasing_order=row[1]
                ),
                supplier=Suppliers(
                    id_supplier=row[2],
                    name=row[3]
                ),
                user=AuthUser(
                    username=row[5]
                ),
                n_delivery_note=row[6],
                obs=row[7],
                created_at=row[8],
            ) for row in data
        ]
