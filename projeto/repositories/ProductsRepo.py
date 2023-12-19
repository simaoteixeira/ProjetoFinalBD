from django.db import connections

from projeto.models import Products, Stock, Warehouses


class ProductsRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_Products")
        data = self.cursor.fetchall()

        return [
            Products(
                id_product=row[0],
                name=row[1],
                description=row[2],
                weight=row[3],
                type=row[4],
                profit_margin=row[5],
                vat=row[6],
                price_cost=row[7],
                price_base=row[8],
                pvp=row[9],
            ) for row in data
        ]

    def find_all_components(self):
        self.cursor.execute("SELECT * FROM V_Products WHERE type = 'COMPONENT'")
        data = self.cursor.fetchall()

        return [
            Products(
                id_product=row[0],
                name=row[1],
                description=row[2],
                weight=row[3],
                type=row[4],
                profit_margin=row[5],
                vat=row[6],
                price_cost=row[7],
                price_base=row[8],
                pvp=row[9],
            ) for row in data
        ]

    def find_all_products(self):
        self.cursor.execute("SELECT * FROM V_Products WHERE type = 'PRODUCT'")
        data = self.cursor.fetchall()

        return [
            Products(
                id_product=row[0],
                name=row[1],
                description=row[2],
                weight=row[3],
                type=row[4],
                profit_margin=row[5],
                vat=row[6],
                price_cost=row[7],
                price_base=row[8],
                pvp=row[9],
            ) for row in data
        ]

    def find_all_stock(self):
        self.cursor.execute("SELECT * FROM V_StockPerProduct")
        data = self.cursor.fetchall()

        return [
            Stock(
                product=
                    Products(
                        id_product=row[0],
                        name=row[1],
                        type=row[5],
                        weight=row[6],
                    ),
                warehouse=
                    Warehouses(
                        id_warehouse=row[2],
                        name=row[3]
                    ),
                quantity=row[4],
            ) for row in data
        ]

    def create(self, name, type, description, weight, vat, profit_margin):
        self.cursor.callproc('create_product', [name, type, description, weight, vat, profit_margin])