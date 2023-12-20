import django_tables2 as tables

from projeto.models import Suppliers


class SelectSupplierTable(tables.Table):
    print("SelectSupplierTable", tables.A("id_supplier"))

    name = tables.Column(verbose_name="Designação", accessor="name")
    nif = tables.Column(verbose_name="NIF", accessor="nif")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_select_supplier_column.html",
        orderable=False
    )

    class Meta:
        model = Suppliers
        attrs = {"class": "table"}
        fields = ("name", "nif")
