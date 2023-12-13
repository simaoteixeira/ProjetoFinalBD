# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ClientInvoiceComponents(models.Model):
    id_client_invoice_component = models.AutoField(primary_key=True)
    id_product = models.ForeignKey('Products', models.DO_NOTHING, db_column='id_product')
    id_client_invoice = models.ForeignKey('ClientInvoices', models.DO_NOTHING, db_column='id_client_invoice')
    quantity = models.IntegerField()
    price_base = models.TextField()  # This field type is a guess.
    vat = models.IntegerField()
    vat_value = models.TextField()  # This field type is a guess.
    discount = models.FloatField()
    discount_value = models.TextField()  # This field type is a guess.
    line_total = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'client_invoice_components'


class ClientInvoices(models.Model):
    id_client_invoice = models.AutoField(primary_key=True)
    id_client = models.ForeignKey('Clients', models.DO_NOTHING, db_column='id_client')
    obs = models.TextField(blank=True, null=True)
    total_base = models.TextField()  # This field type is a guess.
    vat_total = models.TextField()  # This field type is a guess.
    discount_total = models.TextField()  # This field type is a guess.
    expire_date = models.DateTimeField()
    invoice_date = models.DateTimeField()
    invoice_id = models.TextField()
    total = models.TextField()  # This field type is a guess.
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'client_invoices'


class ClientOrderComponents(models.Model):
    id_client_order_components = models.AutoField(primary_key=True)
    id_product = models.ForeignKey('Products', models.DO_NOTHING, db_column='id_product')
    id_client_order = models.ForeignKey('ClientOrders', models.DO_NOTHING, db_column='id_client_order')
    quantity = models.IntegerField()
    price_base = models.TextField()  # This field type is a guess.
    vat = models.IntegerField()
    vat_value = models.TextField()  # This field type is a guess.
    discount = models.FloatField()
    discount_value = models.TextField()  # This field type is a guess.
    line_total = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'client_order_components'


class ClientOrders(models.Model):
    id_client_order = models.AutoField(primary_key=True)
    id_client = models.ForeignKey('Clients', models.DO_NOTHING, db_column='id_client')
    id_sale_order = models.ForeignKey('SalesOrders', models.DO_NOTHING, db_column='id_sale_order', blank=True, null=True)
    total_base = models.TextField()  # This field type is a guess.
    vat_total = models.TextField()  # This field type is a guess.
    discount_total = models.TextField()  # This field type is a guess.
    total = models.TextField()  # This field type is a guess.
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'client_orders'


class Clients(models.Model):
    id_client = models.AutoField(primary_key=True)
    name = models.TextField()
    email = models.TextField()
    nif = models.TextField()
    phone = models.TextField()
    address = models.TextField()
    locality = models.TextField()
    postal_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'clients'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Labors(models.Model):
    id_labor = models.AutoField(primary_key=True)
    title = models.TextField()
    cost = models.FloatField()

    class Meta:
        managed = False
        db_table = 'labors'


class MaterialReceiptComponents(models.Model):
    id_material_receipt_component = models.AutoField(primary_key=True)
    id_material_receipt = models.ForeignKey('MaterialReceipts', models.DO_NOTHING, db_column='id_material_receipt')
    id_warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, db_column='id_warehouse')
    id_product = models.ForeignKey('Products', models.DO_NOTHING, db_column='id_product')
    quantity = models.IntegerField()
    price_base = models.TextField()  # This field type is a guess.
    vat = models.IntegerField()
    vat_value = models.TextField()  # This field type is a guess.
    discount = models.FloatField()
    discount_value = models.TextField()  # This field type is a guess.
    line_total = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'material_receipt_components'


class MaterialReceipts(models.Model):
    id_material_receipt = models.AutoField(primary_key=True)
    supplier_invoice = models.ForeignKey('SupplierInvoices', models.DO_NOTHING, db_column='id_supplier_invoice', blank=True, null=True)
    id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_user')
    id_purchasing_order = models.ForeignKey('PurchasingOrders', models.DO_NOTHING, db_column='id_purchasing_order')
    n_delivery_note = models.TextField()
    total_base = models.TextField()  # This field type is a guess.
    vat_total = models.TextField()  # This field type is a guess.
    discount_total = models.TextField()  # This field type is a guess.
    total = models.TextField()  # This field type is a guess.
    obs = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'material_receipts'


class ProductionOrderComponents(models.Model):
    id_production_order_components = models.AutoField(primary_key=True)
    id_warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, db_column='id_warehouse')
    id_order_production = models.ForeignKey('ProductionOrders', models.DO_NOTHING, db_column='id_order_production')
    id_product = models.ForeignKey('Products', models.DO_NOTHING, db_column='id_product')
    quantity = models.IntegerField()
    price_base = models.TextField()  # This field type is a guess.
    line_total = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'production_order_components'


class ProductionOrders(models.Model):
    id_order_production = models.AutoField(primary_key=True)
    id_labor = models.ForeignKey(Labors, models.DO_NOTHING, db_column='id_labor')
    id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_user')
    id_product = models.ForeignKey('Products', models.DO_NOTHING, db_column='id_product')
    equipment_quantity = models.IntegerField()
    unit_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    production_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    obs = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'production_orders'


class Products(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    type = models.TextField()  # This field type is a guess.
    profit_margin = models.FloatField()
    vat = models.IntegerField()
    price_cost = models.TextField(blank=True, null=True)  # This field type is a guess.
    price_base = models.TextField(blank=True, null=True)  # This field type is a guess.
    pvp = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'products'


class PurchasingOrderComponents(models.Model):
    id_purchasing_order_components = models.AutoField(primary_key=True)
    id_purchasing_order = models.ForeignKey('PurchasingOrders', models.DO_NOTHING, db_column='id_purchasing_order')
    id_product = models.ForeignKey(Products, models.DO_NOTHING, db_column='id_product')
    quantity = models.IntegerField()
    price_base = models.TextField()  # This field type is a guess.
    vat = models.IntegerField()
    vat_value = models.TextField()  # This field type is a guess.
    discount = models.FloatField()
    discount_value = models.TextField()  # This field type is a guess.
    line_total = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'purchasing_order_components'


class PurchasingOrders(models.Model):
    id_purchasing_order = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Suppliers', models.DO_NOTHING, db_column='id_supplier')
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_user')
    total_base = models.TextField()  # This field type is a guess.
    vat_total = models.TextField()  # This field type is a guess.
    discount_total = models.TextField()  # This field type is a guess.
    total = models.TextField()  # This field type is a guess.
    obs = models.TextField(blank=True, null=True)
    delivery_date = models.DateTimeField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'purchasing_orders'


class SalesOrderComponents(models.Model):
    id_sales_order_component = models.AutoField(primary_key=True)
    id_product = models.ForeignKey(Products, models.DO_NOTHING, db_column='id_product')
    id_sale_order = models.ForeignKey('SalesOrders', models.DO_NOTHING, db_column='id_sale_order')
    quantity = models.IntegerField()
    price_base = models.TextField()  # This field type is a guess.
    vat = models.IntegerField()
    vat_value = models.TextField()  # This field type is a guess.
    discount = models.FloatField()
    discount_value = models.TextField()  # This field type is a guess.
    line_total = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sales_order_components'


class SalesOrders(models.Model):
    id_sale_order = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_user')
    id_client_invoice = models.ForeignKey(ClientInvoices, models.DO_NOTHING, db_column='id_client_invoice', blank=True, null=True)
    obs = models.TextField(blank=True, null=True)
    total_base = models.TextField()  # This field type is a guess.
    vat_total = models.TextField()  # This field type is a guess.
    discount_total = models.TextField()  # This field type is a guess.
    total = models.TextField()  # This field type is a guess.
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sales_orders'


class Stock(models.Model):
    id_product = models.OneToOneField(Products, models.DO_NOTHING, db_column='id_product', primary_key=True)  # The composite primary key (id_product, id_warehouse) found, that is not supported. The first column is selected.
    id_warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, db_column='id_warehouse')
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock'
        unique_together = (('id_product', 'id_warehouse'), ('id_product', 'id_warehouse'),)


class StockMovements(models.Model):
    id_stock_movement = models.AutoField(primary_key=True)
    id_product = models.ForeignKey(Products, models.DO_NOTHING, db_column='id_product')
    id_warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, db_column='id_warehouse')
    quantity = models.IntegerField()
    type = models.TextField()
    reason = models.TextField()
    id_reason = models.IntegerField()
    prev_quantity = models.IntegerField()
    pos_quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock_movements'


class SupplierInvoiceComponents(models.Model):
    id_supplier_invoice_component = models.AutoField(primary_key=True)
    id_supplier_invoice = models.ForeignKey('SupplierInvoices', models.DO_NOTHING, db_column='id_supplier_invoice')
    id_product = models.ForeignKey(Products, models.DO_NOTHING, db_column='id_product')
    quantity = models.IntegerField()
    price_base = models.TextField()  # This field type is a guess.
    vat = models.IntegerField()
    vat_value = models.TextField()  # This field type is a guess.
    discount = models.FloatField()
    discount_value = models.TextField()  # This field type is a guess.
    line_total = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'supplier_invoice_components'


class SupplierInvoices(models.Model):
    id_supplier_invoice = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Suppliers', models.DO_NOTHING, db_column='id_supplier')
    obs = models.TextField(blank=True, null=True)
    total_base = models.TextField()  # This field type is a guess.
    vat_total = models.TextField()  # This field type is a guess.
    discount_total = models.TextField()  # This field type is a guess.
    total = models.TextField()  # This field type is a guess.
    expire_date = models.DateTimeField()
    invoice_date = models.DateTimeField()
    invoice_id = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'supplier_invoices'


class Suppliers(models.Model):
    id_supplier = models.AutoField(primary_key=True)
    name = models.TextField()
    email = models.TextField()
    nif = models.TextField()
    phone = models.TextField()
    address = models.TextField()
    locality = models.TextField()
    postal_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'suppliers'


class Warehouses(models.Model):
    id_warehouse = models.AutoField(primary_key=True)
    name = models.TextField()
    location = models.TextField()

    class Meta:
        managed = False
        db_table = 'warehouses'
