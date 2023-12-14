import django_tables2 as tables
from ..models import Products, Stock


class ProductsTable(tables.Table):
    name = tables.Column(verbose_name="Nome", accessor="name")
    weight = tables.Column(verbose_name="Peso", accessor="weight")
    type = tables.Column(verbose_name="Tipo", accessor="type")
    price_base = tables.Column(verbose_name="Preço Base", accessor="price_base")

    class Meta:
        model = Products
        attrs = {"class": "table"}
        fields = ("name", "weight", "type", "price_base")

class StockProductsTable():
    name = tables.Column(verbose_name="Nome", accessor="product.name")
    quantity = tables.Column(verbose_name="Quantidade", accessor="quantity")
    weight = tables.Column(verbose_name="Peso", accessor="product.weight")
    warehouse = tables.Column(verbose_name="Armazém", accessor="warehouse.name")
    #type = tables.Column(verbose_name="Tipo", accessor="product.type")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_tools_column.html",
        orderable=False,
        extra_context={
            'trashButton': True,
        }
    )

    class Meta:
        model = Stock
        attrs = {"class": "table"}
        fields = ("name", "quantity", "weight", "warehouse", "type")