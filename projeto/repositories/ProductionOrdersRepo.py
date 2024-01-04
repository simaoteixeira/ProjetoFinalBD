from django.db import connections

from projeto.models import ProductionOrders, Labors, AuthUser, Products, ProductionOrderComponents


class ProductionOrdersRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_ProductionOrders")
        data = self.cursor.fetchall()

        return [
            ProductionOrders(
                id_order_production=row[0],
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

    def find_by_id(self, id):
        self.cursor.execute("SELECT * FROM V_ProductionOrders WHERE id_order_production = %s", [id])
        data = self.cursor.fetchone()

        return ProductionOrders(
            id_order_production=data[0],
            labor=Labors(
                id_labor=data[1],
                cost=data[2],
            ),
            user=AuthUser(
                id=data[3],
                username=data[4],
            ),
            product=Products(
                id_product=data[5],
                name=data[6],
            ),
            equipment_quantity=data[7],
            production_cost=data[8],
            unit_cost=data[9],
            status=data[10],
            created_at=data[11],
            last_updated=data[12],
            obs=data[13]
        )

    def find_components(self, id):
        self.cursor.execute("SELECT * FROM V_ProductionOrderComponents WHERE id_order_production = %s", [id])
        data = self.cursor.fetchall()

        return [
            ProductionOrderComponents(
                id_production_order_components=row[0],
                id_order_production=ProductionOrders(
                    id_order_production=row[1],
                ),
                product=Products(
                    id_product=row[2],
                    name=row[3],
                ),
                quantity=row[6],
                price_base=row[7],
                total_unit=row[8],
                line_total=row[9],
            ) for row in data
        ]

    def create(self, id_labor, id_user, id_product, equipment_quantity, obs, products):
        print(id_labor, id_user, id_product, equipment_quantity, obs, products)

        self.cursor.execute('SELECT * FROM FN_Create_ProductionOrder(%s, %s, %s, %s, %s, %s)', [id_labor, id_user, id_product, equipment_quantity, products[0]["warehouse"], obs])
        response = self.cursor.fetchone()

        if response[0]:
            id_production_order = response[0]

            for product in products:
                print(id_production_order)
                print(product)
                print(product["id"])
                print(product["warehouse"])
                print(product["quantity"])

                self.cursor.execute('Call PA_InsertLine_ProductionOrder(%s, %s, %s, %s)', [id_production_order, product["id"], product["warehouse"], product["quantity"]])

            return True

    def update_obs(self, id, obs):
        self.cursor.execute('UPDATE production_orders SET obs = %s WHERE id_order_production = %s', [obs, id])
        return True

    def update_status(self, id, status):
        self.cursor.execute('Call PA_Update_ProductionOrderStatus(%s, %s)', [id, status])
        return True