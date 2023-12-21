import django_tables2 as tables

from projeto.models import Suppliers, ClientInvoices


class ClientInvoicesTable(tables.Table):
    number = tables.Column(accessor='invoice_id', verbose_name='Fatura Nº')
    client = tables.Column(accessor='client.name', verbose_name='Cliente')
    total = tables.Column(accessor='total', verbose_name='Valor')
    created_at = tables.Column(accessor='created_at', verbose_name='Data de Criação')
    see = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_column_eye.html",
        orderable=False,
        linkify=('faturaCliente', {'id': tables.A('id_client_invoice')}),
    )

    class Meta:
        model = ClientInvoices
        attrs = {"class": "table"}
        fields = ('number', 'client', 'total', 'created_at')