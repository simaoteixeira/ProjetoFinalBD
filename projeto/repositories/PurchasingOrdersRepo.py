from django.db import connections

from projeto.models import Suppliers, PurchasingOrders, AuthUser, PurchasingOrderComponents, Products


class PurchasingOrdersRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_PurchasingOrders")
        dataPurchasingOrders = self.cursor.fetchall()

        data = [
            PurchasingOrders(
                id_purchasing_order=row[0],
                supplier=Suppliers(
                    id_supplier=row[1],
                    name=row[2],
                ),
                user=AuthUser(
                    username=row[4],
                ),
                delivery_date=row[5],
                created_at=row[6],
                obs=row[7],
                total_base=row[8],
                vat_total=row[9],
                discount_total=row[10],
                total=row[11],
            ) for row in dataPurchasingOrders
        ]

        return data

    def find_by_id(self, id):
        self.cursor.execute("SELECT * FROM V_PurchasingOrders WHERE id_purchasing_order = %s", [id])
        dataPurchasingOrder = self.cursor.fetchone()

        data = PurchasingOrders(
            id_purchasing_order=dataPurchasingOrder[0],
            supplier=Suppliers(
                id_supplier=dataPurchasingOrder[1],
                name=dataPurchasingOrder[2],
            ),
            user=AuthUser(
                username=dataPurchasingOrder[4],
            ),
            delivery_date=dataPurchasingOrder[5],
            created_at=dataPurchasingOrder[6],
            obs=dataPurchasingOrder[7],
            total_base=dataPurchasingOrder[8],
            vat_total=dataPurchasingOrder[9],
            discount_total=dataPurchasingOrder[10],
            total=dataPurchasingOrder[11],
        )

        return data

    def find_by_supplier(self, id):
        self.cursor.execute("SELECT * FROM V_PurchasingOrders WHERE id_supplier = %s", [id])
        dataPurchasingOrder = self.cursor.fetchall()

        data = [
            PurchasingOrders(
                id_purchasing_order=row[0],
                supplier=Suppliers(
                    id_supplier=row[1],
                    name=row[2],
                ),
                user=AuthUser(
                    username=row[4],
                ),
                delivery_date=row[5],
                created_at=row[6],
                obs=row[7],
                total_base=row[8],
                vat_total=row[9],
                discount_total=row[10],
                total=row[11],
            ) for row in dataPurchasingOrder
        ]

        return data

    def find_components(self, id):
        self.cursor.execute("SELECT * FROM V_PurchasingOrderComponents WHERE id_purchasing_order = %s", [id])
        dataPurchasingOrderComponents = self.cursor.fetchall()

        data = [
            PurchasingOrderComponents(
                purchasing_order=PurchasingOrders(
                    id_purchasing_order=row[0],
                ),
                product=Products(
                    id_product=row[1],
                    name=row[2],
                ),
                quantity=row[3],
                price_base=row[4],
                total_unit=row[5],
                vat=row[6],
                vat_value=row[7],
                discount=row[8],
                discount_value=row[9],
                line_total=row[10],
            ) for row in dataPurchasingOrderComponents
        ]

        return data

    def update_obs(self, id, obs):
        self.cursor.execute("UPDATE purchasing_orders SET obs = %s WHERE id_purchasing_order = %s", [obs.strip(), id])

    def create(self, id_supplier, id_user, delivery_date, obs, products=[]):
        self.cursor.execute('SELECT * FROM FN_Create_PurchasingOrder(%s,%s,%s,%s)',
                            [id_supplier, id_user, delivery_date, obs])
        reponse = self.cursor.fetchone()

        if reponse[0]:
            id_purchasing_order = reponse[0]

            print(id_purchasing_order)

            for product in products:
                self.cursor.execute('Call PA_InsertLine_PurchasingOrder(%s, %s, %s, %s, %s, %s)', [
                    id_purchasing_order,
                    product["id"],
                    product["quantity"],
                    product["price_base"],
                    product["vat"] or 0,
                    product["discount"] or 0,
                ])

            return True
