from django.db import connections, models

from projeto.models import Warehouses, Stock, Products


class WarehousesViewModel(models.Model):
    id_warehouse = models.AutoField(primary_key=True)
    name = models.TextField()
    location = models.TextField()
    total_stock = models.IntegerField()

class WarehousesRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_Warehouses")
        data = self.cursor.fetchall()

        return [
            WarehousesViewModel(
                id_warehouse=row[0],
                name=row[1],
                location=row[2],
                total_stock=row[3],
            ) for row in data
        ]

    def get_stock(self, id):
        self.cursor.execute("SELECT * FROM V_Stock WHERE id_warehouse = %s", [id])
        data = self.cursor.fetchone()

        print(data)

        if data is None:
            return None

        return Stock(
            product=(
                Products(
                    id_product=data[0],
                    name=data[3],
                    description=data[4],
                    type=data[5],
                )
            ),
            warehouse=(
                Warehouses(
                    id_warehouse=data[1],
                    name=data[6]
                )
            ),
            quantity=data[2],
        )