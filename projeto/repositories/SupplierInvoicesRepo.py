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
                supplier=Suppliers(
                    id_supplier=row[1],
                    name=row[2],
                    address=row[3],
                    locality=row[4],
                    postal_code=row[5],
                    nif=row[6],
                ),
                invoice_id=row[8],
                invoice_date=row[9],
                expire_date=row[10],
                obs=row[11],
                total_base=row[12],
                vat_total=row[13],
                discount_total=row[14],
                total=row[15],
                created_at=row[16],
            ) for row in data
        ]