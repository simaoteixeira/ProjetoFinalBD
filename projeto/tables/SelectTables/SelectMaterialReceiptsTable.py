import django_tables2 as tables

from projeto.models import MaterialReceipts


class SelectMaterialReceiptsTable(tables.Table):
    id = tables.Column(verbose_name="ID", accessor="id_material_receipt")
    n_delivery_note = tables.Column(verbose_name="N Guia", accessor="n_delivery_note")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_select_materialReceipts_column.html",
        orderable=False
    )

    class Meta:
        model = MaterialReceipts
        attrs = {"class": "table"}
        fields = ['id', 'n_delivery_note']
