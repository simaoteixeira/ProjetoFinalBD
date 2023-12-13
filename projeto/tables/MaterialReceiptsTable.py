import django_tables2 as tables

class MaterialReceiptsTable(tables.Table):
    supplier = tables.Column(accessor='supplier_name', verbose_name='Fornecedor')
    purchase_order = tables.Column(accessor='id_purchasing_order', verbose_name='Ordem de Compra')
    n_delivery_note = tables.Column(accessor='n_delivery_note', verbose_name='N Guia')
    #component_number = tables.Column(accessor='component_number', verbose_name='Nº Componentes')
    total = tables.Column(accessor='total', verbose_name='Total')
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_tools_column.html",
        orderable=False
    )

    class Meta:
        attrs = {"class": "table"}
        fields = ('supplier', 'purchase_order', 'n_delivery_note', 'total')