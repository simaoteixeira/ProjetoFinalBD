import django_tables2 as tables

from projeto.models import MaterialReceipts, SalesOrders


class SelectSalesOrdersTable(tables.Table):
    id = tables.Column(verbose_name="ID", accessor="id_sale_order")
    created_at = tables.DateColumn(verbose_name="Data", accessor="created_at")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_select_SalesOrder_column.html",
        orderable=False
    )

    class Meta:
        model = SalesOrders
        attrs = {"class": "table"}
        fields = ["id", "created_at"]
