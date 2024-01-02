from django.db import connections

from projeto.models import Suppliers, Clients, StockMovements, Products, Warehouses


class StockMovmentsRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_Movements")
        data = self.cursor.fetchall()

        return [
            StockMovements(
                id_stock_movement=row[0],
                quantity=row[1],
                type=row[2],
                reason=row[3],
                id_reason=row[4],
                prev_quantity=row[5],
                pos_quantity=row[6],
                created_at=row[7],
                product=Products(
                    id_product=row[8],
                    name=row[9],
                ),
                warehouse=Warehouses(
                    id_warehouse=row[10],
                    name=row[11],
                ),
            ) for row in data
        ]