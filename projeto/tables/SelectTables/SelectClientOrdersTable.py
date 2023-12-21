import django_tables2 as tables

from projeto.models import Products, ClientOrders


class SelectClientOrdersTable(tables.Table):
    id = tables.Column(verbose_name="ID", accessor="id_client_order")
    created_at = tables.Column(verbose_name="Data", accessor="created_at")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_select_clientOrders_column.html",
        orderable=False
    )

    class Meta:
        model = ClientOrders
        attrs = {"class": "table"}
        fields = ("id", "created_at")
