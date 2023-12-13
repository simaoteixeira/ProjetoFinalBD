import django_tables2 as tables

from projeto.models import Suppliers


class SupplierInvoicesTable(tables.Table):
    number = tables.Column(accessor='invoice_id', verbose_name='Fatura Nº')
    supplier = tables.Column(accessor='supplier.name', verbose_name='Fornecedor')
    component_total = tables.Column(accessor='component_total', verbose_name='Total de Componentes')
    total = tables.Column(accessor='total', verbose_name='Valor')
    created_at = tables.Column(accessor='created_at', verbose_name='Data de Criação')
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_tools_column.html",
        orderable=False,
        extra_context={
            'trashButton': True
        }
    )

    class Meta:
        model = Suppliers
        attrs = {"class": "table"}
        fields = ('number', 'supplier', 'component_total', 'total', 'created_at')