from django.db import connections

from projeto.models import SalesOrders, AuthUser, SalesOrderComponents, Products


class SalesOrdersRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute('SELECT * FROM V_SalesOrders')

        data = self.cursor.fetchall()

        return [
            SalesOrders(
                id_sale_order=row[0],
                user=AuthUser(
                    id=row[1],
                    username=row[2],
                ),
                created_at=row[5],
                obs=row[6],
                total_base=row[7],
            ) for row in data
        ]

    def find_by_client(self, id):
        self.cursor.execute("SELECT * FROM V_SalesOrders WHERE %s = ANY (client_orders)", [id])
        data = self.cursor.fetchall()

        return [
            SalesOrders(
                id_sale_order=row[0],
                user=AuthUser(
                    id=row[1],
                    username=row[2],
                ),
                created_at=row[5],
                obs=row[6],
                total_base=row[7],
            ) for row in data
        ]

    def find_components_by_ids(self, ids):
        print(ids)
        self.cursor.execute("SELECT * FROM V_SalesOrderComponents WHERE id_sale_order = ANY(%s)", [ids])
        data = self.cursor.fetchall()

        return [
            SalesOrderComponents(
                id_sales_order_component=row[0],
                sale_order=SalesOrders(
                    id_sale_order=row[1]
                ),
                product=Products(
                    id_product=row[2],
                    name=row[3]
                ),
                quantity=row[4],
                price_base=row[5],
                total_unit=row[6],
                vat=row[7],
                vat_value=row[8],
                discount=row[9],
                discount_value=row[10],
                line_total=row[11],
            ) for row in data
        ]

    def create(self, id_user, obs, products, id_client_order=[]):
        self.cursor.execute("SELECT * FROM FN_Create_SalesOrder(%s, %s, %s)", [id_user, id_client_order, obs or ''])
        result = self.cursor.fetchone()

        if result[0]:
            id_sales_order = result[0]

            for product in products:
                self.cursor.execute("Call PA_InsertLine_SalesOrder(%s, %s, %s, %s, %s, %s)",
                                    [id_sales_order, product['id'], product['quantity'], product['price_base'],
                                     product['vat'], product['discount']])

            return True

    def update_obs(self, id, obs):
        self.cursor.execute("UPDATE sales_orders SET obs = %s WHERE id_sale_order = %s", [obs, id])
