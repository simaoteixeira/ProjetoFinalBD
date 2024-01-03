from django.db import connections, models

from projeto.models import MaterialReceipts, Suppliers, AuthUser, PurchasingOrders, MaterialReceiptComponents, Products, \
    Warehouses


class MaterialReceiptsView(MaterialReceipts):
    supplier = models.ForeignKey('Suppliers', models.DO_NOTHING, db_column='id_supplier')


class MaterialReceiptsRepo:
    def __init__(self, connection='default'):
        self.cursor = connections[connection].cursor()

    def find_all(self):
        self.cursor.execute("SELECT * FROM V_MaterialReceipts")
        data = self.cursor.fetchall()

        return [
            MaterialReceiptsView(
                id_material_receipt=row[0],
                purchasing_order=PurchasingOrders(
                    id_purchasing_order=row[1]
                ),
                supplier=Suppliers(
                    id_supplier=row[2],
                    name=row[3]
                ),
                user=AuthUser(
                    username=row[5]
                ),
                n_delivery_note=row[6],
                obs=row[7],
                created_at=row[8],
                total_base=row[9],
                vat_total=row[10],
                discount_total=row[11],
                total=row[12],
            ) for row in data
        ]

    def find_by_id(self, id):
        self.cursor.execute("SELECT * FROM V_MaterialReceipts WHERE id_material_receipt = %s", [id])
        data = self.cursor.fetchone()
        print(data)

        return MaterialReceiptsView(
            id_material_receipt=data[0],
            purchasing_order=PurchasingOrders(
                id_purchasing_order=data[1]
            ),
            supplier=Suppliers(
                id_supplier=data[2],
                name=data[3]
            ),
            user=AuthUser(
                username=data[5]
            ),
            n_delivery_note=data[6],
            obs=data[7],
            created_at=data[8],
            total_base=data[9],
            vat_total=data[10],
            discount_total=data[11],
            total=data[12],
        )

    def find_by_supplier(self, id):
        self.cursor.execute("SELECT * FROM V_MaterialReceipts WHERE id_supplier = %s", [id])
        data = self.cursor.fetchall()

        return [
            MaterialReceiptsView(
                id_material_receipt=row[0],
                purchasing_order=PurchasingOrders(
                    id_purchasing_order=row[1]
                ),
                supplier=Suppliers(
                    id_supplier=row[2],
                    name=row[3]
                ),
                user=AuthUser(
                    username=row[5]
                ),
                n_delivery_note=row[6],
                obs=row[7],
                created_at=row[8],
                total_base=row[9],
                vat_total=row[10],
                discount_total=row[11],
                total=row[12],
            ) for row in data
        ]

    def find_components_by_ids(self, ids):
        #Convert ids to tuple
        #ids = tuple(ids)
        #print(ids)

        self.cursor.execute("SELECT * FROM V_MaterialReceiptComponents WHERE id_material_receipt = ANY(%s)", [ids])
        data = self.cursor.fetchall()

        print(data)

        return [
            MaterialReceiptComponents(
                id_material_receipt_component=row[0],
                product=Products(
                    id_product=row[1],
                    name=row[2]
                ),
                warehouse=Warehouses(
                    id_warehouse=row[3],
                    name=row[4]
                ),
                quantity=row[5],
                price_base=row[6],
                total_unit=row[7],
                vat=row[8],
                vat_value=row[9],
                discount=row[10],
                discount_value=row[11],
                line_total=row[12],
                id_material_receipt=MaterialReceipts(
                    id_material_receipt=row[13]
                )
            ) for row in data
        ]

    def create(self, id_user, id_purchasing_order, n_delivery_note, obs, products=[]):
        print(id_user, id_purchasing_order, n_delivery_note, obs, products)
        self.cursor.execute("SELECT * FROM FN_Create_MaterialReceipts(%s,%s,%s,%s)", [id_user, id_purchasing_order, n_delivery_note, obs or ''])
        response = self.cursor.fetchone()

        if (response[0]):
            id_material_receipt = response[0]

            for product in products:
                self.cursor.execute("Call PA_InsertLine_MaterialReceipt(%s, %s, %s, %s, %s, %s, %s)", [
                    id_material_receipt,
                    product["id"],
                    product["warehouse"],
                    product["quantity"],
                    product["price_base"] or 0,
                    product["vat"] or 0,
                    product["discount"] or 0
                ])

            return True

    def update_obs(self, id, obs):
        self.cursor.execute("UPDATE material_receipts SET obs = %s WHERE id_material_receipt = %s", [obs.strip(), id])

    def find_components(self, id):
        self.cursor.execute("SELECT * FROM V_MaterialReceiptComponents WHERE id_material_receipt = %s", [id])
        data = self.cursor.fetchall()

        return [
            MaterialReceiptComponents(
                id_material_receipt_component=row[0],
                product=Products(
                    id_product=row[1],
                    name=row[2]
                ),
                warehouse=Warehouses(
                    id_warehouse=row[3],
                    name=row[4]
                ),
                quantity=row[5],
                price_base=row[6],
                total_unit=row[7],
                vat=row[8],
                vat_value=row[9],
                discount=row[10],
                discount_value=row[11],
                line_total=row[12],
                id_material_receipt=MaterialReceipts(
                    id_material_receipt=row[13]
                )
            ) for row in data
        ]