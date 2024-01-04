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

    def find_by_id(self, id):
        self.cursor.execute("SELECT * FROM V_Products WHERE id_product = %s", [id])
        data = self.cursor.fetchone()

        return Products(
            id_product=data[0],
            name=data[1],
            description=data[2],
            weight=data[3],
            type=data[4],
            profit_margin=data[5],
            vat=data[6],
            price_cost=data[7],
            price_base=data[8],
            pvp=data[9],
        )

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
        self.cursor.execute("SELECT * FROM V_Products WHERE type = 'EQUIPMENT'")
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
        print(data)
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

    def find_product_stock_by_warehouse(self, id_product):
        self.cursor.execute("SELECT * FROM V_StockPerProduct WHERE id_product = %s", [id_product])
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
        print(name, type, description, weight, vat, profit_margin)
        self.cursor.execute("SELECT FN_Create_Product(%s,%s,%s,%s,%s,%s)",
                            [name, description, type, weight, vat, profit_margin])
        data = self.cursor.fetchall()

    def update_obs(self, id, description):
        self.cursor.execute("UPDATE products SET description = %s WHERE  = %s", [description, id])

    def edit(self, id_product, name, description, weight, vat, profit_margin):
        self.cursor.execute("Call PA_Update_Product(%s,%s,%s,%s,%s,%s)",
                            [id_product, name, description, weight, vat, profit_margin])
        return True

    def import_products(self, file):
        print(file)
        self.cursor.execute("SELECT FN_Create_Product_From_JSON(%t)", [file])
        data = self.cursor.fetchall()
        return data[0][0]
