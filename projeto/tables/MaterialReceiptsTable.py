import django_tables2 as tables

class MaterialReceiptsTable(tables.Table):
    supplier = tables.Column(accessor='supplier.name', verbose_name='Fornecedor')
    purchase_order = tables.Column(accessor='purchasing_order.id_purchasing_order', verbose_name='Ordem de Compra')
    n_delivery_note = tables.Column(accessor='n_delivery_note', verbose_name='N Guia')
    created_at = tables.Column(accessor='created_at', verbose_name='Criada a')
    see = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_column_eye.html",
        orderable=False,
        linkify=('recessaoMaterial', {'id': tables.A('id_material_receipt')}),
    )

    class Meta:
        attrs = {"class": "table"}
        fields = ('supplier', 'purchase_order', 'n_delivery_note')