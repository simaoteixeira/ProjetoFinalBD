from django.db import connections, models

from projeto.models import MaterialReceipts

class MaterialReceiptsView(MaterialReceipts):
    supplier_name = models.TextField()

class MaterialReceiptsRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_MaterialReceipts")
        data = self.cursor.fetchall()

        return [
            MaterialReceiptsView(
                id_material_receipt=row[0],
                supplier_invoice=row[1],
                id_user=row[2],
                id_purchasing_order=row[3],
                n_delivery_note=row[4],
                total_base=row[5],
                vat_total=row[6],
                discount_total=row[7],
                total=row[8],
                obs=row[9],
                created_at=row[10],
                supplier_name=row[11]
            ) for row in data
        ]
