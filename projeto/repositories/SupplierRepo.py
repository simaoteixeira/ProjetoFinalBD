from django.db import connections

from projeto.models import Suppliers


class SupplierRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def create(self, name, email, nif, phone, address, locality, postal_code):
        self.cursor.execute(f"Call PA_Create_Supplier(%s, %s, %s, %s, %s, %s, %s)",
                            [name, email, nif, phone, address, locality, postal_code])

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

    def find_by_id(self, id):
        self.cursor.execute(f"SELECT * FROM V_Suppliers WHERE id_supplier = {id}")
        data = self.cursor.fetchone()

        return Suppliers(
            id_supplier=data[0],
            name=data[1],
            email=data[2],
            nif=data[3],
            phone=data[4],
            address=data[5],
            locality=data[6],
            postal_code=data[7]
        )

    def edit(self, id_supplier, name, email, nif, phone, address, locality, postal_code):
        self.cursor.execute(f"Call PA_Update_Supplier(%s, %s, %s, %s, %s, %s, %s, %s)",
                            [id_supplier, name, email, nif, phone, address, locality, postal_code])
