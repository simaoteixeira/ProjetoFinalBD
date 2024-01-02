import django_tables2 as tables

from projeto.models import PurchasingOrders


class SelectPurchasingOrdersTable(tables.Table):
    id = tables.Column(verbose_name="ID", accessor="id_purchasing_order")
    date = tables.DateColumn(verbose_name="Data", accessor="created_at")
    total = tables.Column(verbose_name="Valor Total", accessor="total")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_select_purchasingOrder_column.html",
        orderable=False
    )

    class Meta:
        model = PurchasingOrders
        attrs = {"class": "table"}
        fields = ['id', 'total']
