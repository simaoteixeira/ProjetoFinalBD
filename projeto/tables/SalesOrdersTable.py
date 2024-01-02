import django_tables2 as tables

from projeto.models import SalesOrders


class SalesOrdersTable(tables.Table):
    id_sale_order = tables.Column(verbose_name="ID Guia", accessor="id_sale_order")
    total_base = tables.Column(verbose_name="Valor Base Total", accessor="total_base")
    user = tables.Column(verbose_name="Registado por", accessor="user.username")
    created_at = tables.DateColumn(verbose_name="Data", accessor="created_at")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_tools_column.html",
        orderable=False,
        extra_context={
            'trashButton': True,
        }
    )

    class Meta:
        model = SalesOrders
        attrs = {"class": "table"}
        fields = (
            "id_sale_order",
            "total_base",
            "user",
            "created_at",
        )
