from django.db import connections

from projeto.models import ClientOrders, Clients, ClientOrderComponents, Products


class ClientOrdersRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_ClientOrders")
        data = self.cursor.fetchall()

        return [ClientOrders(
            id_client_order=row[0],
            client=Clients(
                id_client=row[1],
                name=row[2],
            ),
            obs=row[3],
            total_base=row[4],
            created_at=row[5],
            vat_total=row[6],
            discount_total=row[7],
            total=row[8],
        ) for row in data]

    def find_by_id(self, id):
        self.cursor.execute("SELECT * FROM V_ClientOrders WHERE id_client_order = %s", [id])
        data = self.cursor.fetchone()

        return ClientOrders(
            id_client_order=data[0],
            client=Clients(
                id_client=data[1],
                name=data[2],
            ),
            obs=data[3],
            total_base=data[4],
            created_at=data[5],
            vat_total=data[6],
            discount_total=data[7],
            total=data[8],
        )

    def find_by_client(self, client):
        self.cursor.execute("SELECT * FROM V_ClientOrders WHERE id_client = %s", [client])
        data = self.cursor.fetchall()

        return [ClientOrders(
            id_client_order=row[0],
            client=Clients(
                id_client=row[1],
                name=row[2],
            ),
            obs=row[3],
            total_base=row[4],
            created_at=row[5],
            vat_total=row[6],
            discount_total=row[7],
            total=row[8],
        ) for row in data]

    def find_components_by_ids(self, ids):
        self.cursor.execute("SELECT * FROM V_ClientOrdersComponents WHERE id_client_order = ANY(%s)", [ids])
        data = self.cursor.fetchall()


        return [ClientOrderComponents(
            id_client_order_components=row[0],
            client_order=ClientOrders(
                id_client_order=row[1],
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
            line_total=row[11],
        ) for row in data]

    def find_components(self, id):
        self.cursor.execute("SELECT * FROM V_ClientOrdersComponents WHERE id_client_order = %s", [id])
        data = self.cursor.fetchall()

        return [ClientOrderComponents(
            id_client_order_components=row[0],
            client_order=ClientOrders(
                id_client_order=row[1],
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
            line_total=row[11],
        ) for row in data]

    def create(self, client, obs, products):
        self.cursor.execute("SELECT * FROM FN_Create_ClientOrders(%s, %s)", [client, obs or ''])
        response = self.cursor.fetchone()

        if response[0]:
            client_order_id = response[0]

            for product in products:
                self.cursor.execute("Call PA_InsertLine_ClientOrders(%s, %s, %s, %s, %s, %s)", [
                    client_order_id,
                    product['id'],
                    product['quantity'],
                    product['price_base'],
                    product['vat'],
                    product['discount'] or 0,
                ])

            return True

    def update_obs(self, id, obs):
        self.cursor.execute("UPDATE client_orders SET obs = %s WHERE id_client_order = %s", [obs, id])
        return True
