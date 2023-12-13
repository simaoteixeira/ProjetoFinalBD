from django.db import connections, models

from projeto.models import MaterialReceipts

class MaterialReceiptsView(models.Model):
    id_material_receipt = models.AutoField(primary_key=True)
    supplier_invoice = models.ForeignKey('SupplierInvoices', models.DO_NOTHING, db_column='id_supplier_invoice',
                                         blank=True, null=True)
    id_user = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='id_user')
    id_purchasing_order = models.ForeignKey('PurchasingOrders', models.DO_NOTHING, db_column='id_purchasing_order')
    n_delivery_note = models.TextField()
    total_base = models.TextField()  # This field type is a guess.
    vat_total = models.TextField()  # This field type is a guess.
    discount_total = models.TextField()  # This field type is a guess.
    total = models.TextField()  # This field type is a guess.
    obs = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    supplier_name = models.TextField()


class MaterialReceiptsRepo:
    def __init__(self):
        self.cursor = connections['default'].cursor()

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
