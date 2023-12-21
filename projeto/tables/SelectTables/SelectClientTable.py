import django_tables2 as tables

from projeto.models import Suppliers, Clients


class SelectClientTable(tables.Table):
    name = tables.Column(verbose_name="Designação", accessor="name")
    nif = tables.Column(verbose_name="NIF", accessor="nif")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_select_client_column.html",
        orderable=False
    )

    class Meta:
        model = Clients
        attrs = {"class": "table"}
        fields = ("name", "nif")
