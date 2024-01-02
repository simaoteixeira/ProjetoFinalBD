import django_tables2 as tables

from projeto.models import Suppliers


class SupplierInvoicesTable(tables.Table):
    number = tables.Column(accessor='invoice_id', verbose_name='Fatura Nº')
    supplier = tables.Column(accessor='supplier.name', verbose_name='Fornecedor')
    total = tables.Column(accessor='total', verbose_name='Valor')
    created_at = tables.DateColumn(accessor='created_at', verbose_name='Data de Criação')
    see = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_column_eye.html",
        orderable=False,
        linkify=('fatura', {'id': tables.A('id_supplier_invoice')}),
    )

    class Meta:
        model = Suppliers
        attrs = {"class": "table"}
        fields = ('number', 'supplier', 'total', 'created_at')