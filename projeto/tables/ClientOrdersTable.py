import django_tables2 as tables

from projeto.models import ClientOrders


class ClientOrdersTable(tables.Table):
    id_client_order = tables.Column(verbose_name="ID Encomenda", accessor="id_client_order")
    client = tables.Column(verbose_name="Encomendado por", accessor="client.name")
    total_base = tables.Column(verbose_name="Valor Base Produção (€)", accessor="total_base")
    created_at = tables.Column(verbose_name="Data de Criação", accessor="created_at")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_tools_column.html",
        orderable=False,
        extra_context={
            'trashButton': True,
        }
    )

    class Meta:
        model = ClientOrders
        attrs = {"class": "table"}
        fields = ("id_client_order", "client", "total_base", "created_at")
