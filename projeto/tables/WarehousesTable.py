import django_tables2 as tables
from ..models import Labors, Warehouses, Stock


class WarehousesTable(tables.Table):
    id = tables.Column(verbose_name="Codigo", accessor="id_warehouse")
    name = tables.Column(verbose_name="Nome", accessor="name")
    location = tables.Column(verbose_name="Localização", accessor="location")
    total_stock = tables.Column(verbose_name="Produtos em Stock", accessor="total_stock")
    see = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_column_eye.html",
        orderable=False,
        linkify=('armazem', {'id': tables.A('id_warehouse')}),
    )

    class Meta:
        model = Warehouses
        attrs = {"class": "table"}
        fields = ("id", "name", "location", 'total_stock')

class WarehousesStockTable(tables.Table):
    product = tables.Column(verbose_name="Designação", accessor="product.name")
    quantity = tables.Column(verbose_name="Quantidade", accessor="quantity")
    type = tables.Column(verbose_name="Tipo", accessor="product.type")
    warehouse = tables.Column(verbose_name="Armazém", accessor="warehouse.name")
    see = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_column_eye.html",
        orderable=False,
        linkify=('produto', {'id': tables.A('product.id_product')}),
    )

    class Meta:
        model = Stock
        attrs = {"class": "table"}
        fields = ("product", "quantity", "type", "warehouse")