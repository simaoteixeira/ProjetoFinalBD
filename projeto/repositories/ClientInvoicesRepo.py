from django.db import connections

from projeto.models import SupplierInvoices, Suppliers, SupplierInvoiceComponents, Products, ClientInvoices, Clients, \
    ClientInvoiceComponents


class ClientInvoicesRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_ClientInvoices")
        data = self.cursor.fetchall()

        return [
            ClientInvoices(
                id_client_invoice=row[0],
                client=Clients(
                    id_client=row[1],
                    name=row[2],
                    address=row[3],
                    locality=row[4],
                    postal_code=row[5],
                    nif=row[6],
                ),
                invoice_date=row[8],
                expire_date=row[9],
                obs=row[10],
                total_base=row[11],
                vat_total=row[12],
                discount_total=row[13],
                total=row[14],
                created_at=row[15]
            ) for row in data
        ]

    def find_by_id(self, id):
        self.cursor.execute("SELECT * FROM V_ClientInvoices WHERE id_client_invoice = %s", [id])
        data = self.cursor.fetchone()

        return ClientInvoices(
                id_client_invoice=data[0],
                client=Clients(
                    id_client=data[1],
                    name=data[2],
                    address=data[3],
                    locality=data[4],
                    postal_code=data[5],
                    nif=data[6],
                ),
                invoice_date=data[8],
                expire_date=data[9],
                obs=data[10],
                total_base=data[11],
                vat_total=data[12],
                discount_total=data[13],
                total=data[14],
                created_at=data[15],
        )

    def find_components(self, id):
        self.cursor.execute("SELECT * FROM V_ClientInvoicesComponents WHERE id_client_invoice = %s", [id])
        data = self.cursor.fetchall()

        return [
            ClientInvoiceComponents(
                id_client_invoice_component=row[0],
                client_invoice=ClientInvoices(
                    id_client_invoice=row[1],
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

    def create(self, id_client, invoice_date, expire_date, obs, products, id_sales_order=[]):
        self.cursor.execute("SELECT * FROM FN_Create_ClientInvoice(%s, %s, %s, %s, %s, %s)", [id_sales_order, id_client, invoice_date, expire_date, obs])

        result = self.cursor.fetchone()

        if result[0]:
            id_client_invoice = result[0]

            for product in products:
                self.cursor.execute("Call PA_InsertLine_ClientInvoice(%s, %s, %s, %s, %s, %s)", [
                    id_client_invoice,
                    product["id"],
                    product["quantity"],
                    product["price_base"] or 0,
                    product["vat"] or 0,
                    product["discount"] or 0
                ])

    def update_obs(self, id, obs):
        self.cursor.execute("UPDATE client_invoices SET obs = %s WHERE id_client_invoice = %s", [obs, id])