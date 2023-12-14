from django.db import connections

from projeto.models import SupplierInvoices, Suppliers


class SupplierInvoicesRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_SupplierInvoices")
        data = self.cursor.fetchall()

        return [
            SupplierInvoices(
                id_supplier_invoice=row[0],
                supplier=(Suppliers(
                    name=row[11],
                )),
                invoice_id=row[2],
                invoice_date=row[3],
                expire_date=row[4],
                total_base=row[5],
                vat_total=row[6],
                discount_total=row[7],
                total=row[8],
                obs=row[9],
                created_at=row[10],
            ) for row in data
        ]