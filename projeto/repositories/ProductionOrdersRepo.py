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