from django.db import connections

from projeto.models import ProductionOrders, Labors, AuthUser, Products


class ProductionOrdersRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_ProductionOrders")
        data = self.cursor.fetchall()

        #NOT FINISHED
        return [
            ProductionOrders(
                id_production_order=row[0],
                labor=Labors(
                    id_labor=row[1],
                    cost=row[2],
                ),
                user=AuthUser(
                    id=row[3],
                    username=row[4],
                ),
                product=Products(
                    id_product=row[5],
                    name=row[6],
                ),
                equipment_quantity=row[7],
                production_cost=row[8],
                unit_cost=row[9],
                status=row[10],
                created_at=row[11],
                last_updated=row[12],
                obs=row[13]
            ) for row in data
        ]

    def create(self, id_labor, id_user, id_product, equipment_quantity, obs, products):
        print(id_labor, id_user, id_product, equipment_quantity, obs, products)
        self.cursor.callproc('FN_Create_ProductionOrder', [id_labor, id_user, id_product, equipment_quantity, obs])
        response = self.cursor.fetchone()

        if response[0]:
            id_production_order = response[0]

            for product in products:
                self.cursor.execute('Call PA_InsertLine_ProductionOrder(%s, %s, %s, %s, %s)', [id_production_order, product["id"], product["warehouse"], product["quantity"]])

            return True