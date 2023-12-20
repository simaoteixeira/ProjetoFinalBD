import django_tables2 as tables

from projeto.models import Products


class SelectProductsTable(tables.Table):
    name = tables.Column(verbose_name="Designação", accessor="name")
    price_cost = tables.Column(verbose_name="Preço de Custo", accessor="price_cost")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_select_component_column.html",
        orderable=False
    )

    class Meta:
        model = Products
        attrs = {"class": "table"}
        fields = ("name", "price_cost")
