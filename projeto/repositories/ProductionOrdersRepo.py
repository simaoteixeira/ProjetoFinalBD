from django.db import connections

from projeto.models import ProductionOrders


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
                product=row[1],
                id_warehouse=row[2],
                quantity=row[3],
                date=row[4],
                status=row[5],
                product_name=row[6],
                warehouse_name=row[7],
            ) for row in data
        ]