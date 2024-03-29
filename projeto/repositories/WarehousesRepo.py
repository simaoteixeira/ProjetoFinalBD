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

    def find_by_id(self, id):
        self.cursor.execute("SELECT * FROM V_Warehouses WHERE id_warehouse = %s", [id])
        data = self.cursor.fetchone()

        if data is None:
            return None

        return WarehousesViewModel(
            id_warehouse=data[0],
            name=data[1],
            location=data[2],
            total_stock=data[3],
        )

    def get_stock(self, id):
        self.cursor.execute("SELECT * FROM V_StockPerProduct WHERE id_warehouse = %s", [id])
        data = self.cursor.fetchall()

        print(data)

        if data is None:
            return None

        return [
            Stock(
                product=Products(
                    id_product=row[0],
                    name=row[1],
                    type=row[5],
                    weight=row[6],
                ),
                warehouse=Warehouses(
                    id_warehouse=row[2],
                    name=row[3]
                ),
                quantity=row[4],
            ) for row in data
        ]

    def create(self, name, location):
        self.cursor.execute("Call PA_Create_Warehouse(%s, %s)", [name, location])

    def update(self, id, name, location):
        self.cursor.execute("Call PA_Update_Warehouse(%s, %s, %s)", [id, name, location])
