import django_tables2 as tables

from projeto.models import Warehouses


class SelectWarehousesTable(tables.Table):
    name = tables.Column(verbose_name="Designação", accessor="name")
    location = tables.Column(verbose_name="Localização", accessor="location")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_select_warehouse_column.html",
        orderable=False
    )

    class Meta:
        model = Warehouses
        attrs = {"class": "table"}
        fields = ("name", "location")
