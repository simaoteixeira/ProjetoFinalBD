from django.db import connections

from projeto.models import SupplierInvoices, Suppliers, SupplierInvoiceComponents, Products


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

    def find_by_id(self, id):
        self.cursor.execute("SELECT * FROM V_SupplierInvoices WHERE id_supplier_invoice = %s", [id])
        data = self.cursor.fetchone()

        return SupplierInvoices(
            id_supplier_invoice=data[0],
            supplier=Suppliers(
                id_supplier=data[1],
                name=data[2],
                address=data[3],
                locality=data[4],
                postal_code=data[5],
                nif=data[6],
            ),
            material_receptions=data[7],
            invoice_id=data[8],
            invoice_date=data[9],
            expire_date=data[10],
            obs=data[11],
            total_base=data[12],
            vat_total=data[13],
            discount_total=data[14],
            total=data[15],
            created_at=data[16],
        )

    def find_components(self, id):
        self.cursor.execute("SELECT * FROM V_SupplierInvoiceComponents WHERE id_supplier_invoice = %s", [id])
        data = self.cursor.fetchall()

        return [
            SupplierInvoiceComponents(
                id_supplier_invoice_component=row[0],
                supplier_invoice=SupplierInvoices(
                    id_supplier_invoice=row[1],
                ),
                product=Products(
                    id_product=row[2],
                    name=row[3],
                ),
                quantity=row[4],
                price_base=row[5],
                total_unit=row[6],
                vat=row[7],
                vat_value=row[8],
                discount=row[9],
                discount_value=row[10],
                line_total=row[11]
            ) for row in data
        ]

    def create(self, id_supplier, invoice_id, invoice_date, expire_date, obs, products, id_material_receipt=[]):
        id_material_receipt = [int(i) for i in id_material_receipt]
        self.cursor.execute(f"SELECT * FROM FN_Create_SupplierInvoice(%s, %s, %s, %s, %s, %s)", [id_material_receipt, id_supplier, invoice_id, invoice_date, expire_date, obs])

        result = self.cursor.fetchone()

        if result[0]:
            id_supplier_invoice = result[0]

            for product in products:
                self.cursor.execute("Call PA_InsertLine_SupplierInvoice(%s, %s, %s, %s, %s, %s)", [
                    id_supplier_invoice,
                    product["id"],
                    product["quantity"],
                    product["price_base"] or 0,
                    product["vat"] or 0,
                    product["discount"] or 0
                ])

    def update_obs(self, id, obs):
        self.cursor.execute("UPDATE SupplierInvoices SET obs = %s WHERE id_supplier_invoice = %s", [obs, id])