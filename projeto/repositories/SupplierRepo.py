from django.db import connections

from projeto.models import Suppliers


class SupplierRepo:
    def __init__(self):
        self.cursor = connections['default'].cursor()

    def create(self, name, email, nif, phone, address, locality, postal_code):
        self.cursor.execute(f"Call PA_Create_Supplier('{name}', '{email}', '{nif}', '{phone}', '{address}', '{locality}', '{postal_code}')")

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_Suppliers")
        data = self.cursor.fetchall()

        return [
            Suppliers(
                id_supplier=supplier[0],
                name=supplier[1],
                email=supplier[2],
                nif=supplier[3],
                phone=supplier[4],
                address=supplier[5],
                locality=supplier[6],
                postal_code=supplier[7]
            ) for supplier in data
        ]