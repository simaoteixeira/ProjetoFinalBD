import django_tables2 as tables

from projeto.models import ClientOrders


class ClientOrdersTable(tables.Table):
    id_client_order = tables.Column(verbose_name="ID Encomenda", accessor="id_client_order")
    client = tables.Column(verbose_name="Encomendado por", accessor="client.name")
    total_base = tables.Column(verbose_name="Valor Base Produção (€)", accessor="total_base")
    created_at = tables.DateColumn(verbose_name="Data de Criação", accessor="created_at")
    see = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_column_eye.html",
        orderable=False,
        linkify=('encomendaCliente', {'id': tables.A('id_client_order')}),
    )

    class Meta:
        model = ClientOrders
        attrs = {"class": "table"}
        fields = ("id_client_order", "client", "total_base", "created_at")
