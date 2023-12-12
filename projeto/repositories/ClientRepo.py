from django.db import connections

from projeto.models import Suppliers, Clients


class ClientRepo:
    def __init__(self):
        self.cursor = connections['default'].cursor()

    def create(self, name, email, nif, phone, address, locality, postal_code):
        self.cursor.execute(f"Call PA_Create_Client('{name}', '{email}', '{nif}', '{phone}', '{address}', '{locality}', '{postal_code}')")

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_Clients")
        data = self.cursor.fetchall()

        return [
            Clients(
                id_client=client[0],
                name=client[1],
                email=client[2],
                nif=client[3],
                phone=client[4],
                address=client[5],
                locality=client[6],
                postal_code=client[7]
            ) for client in data
        ]