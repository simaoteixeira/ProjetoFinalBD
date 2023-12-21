import django_tables2 as tables
from django.urls import reverse
from ..models import PurchasingOrders, PurchasingOrderComponents


class PurchasingOrdersTable(tables.Table):
    supplier = tables.Column(accessor='supplier.name', verbose_name='Fornecedor')
    total = tables.Column(accessor='total', verbose_name='Valor')
    delivery_date = tables.Column(accessor='delivery_date', verbose_name='Data Possivel de entrega')
    user = tables.Column(accessor='user.username', verbose_name='Registado por')
    created_at = tables.Column(accessor='created_at', verbose_name='Data de Criação do Pedido')
    see = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_column_eye.html",
        orderable=False,
        linkify=('pedidoCompra', {'id': tables.A('id_purchasing_order')}),
    )


    class Meta:
        model = PurchasingOrders
        attrs = {"class": "table"}
        fields = ('supplier', 'total', 'delivery_date', 'user', 'created_at')

class PurchasingOrdersProductsTable(tables.Table):
    id = tables.Column(accessor='product.id_product', verbose_name='ID Produto')
    name = tables.Column(accessor='product.name', verbose_name='Designação')
    quantity = tables.Column(accessor='quantity', verbose_name='Quantidade')
    price_base = tables.Column(accessor='price_base', verbose_name='Valor Unit.')
    total_unit = tables.Column(accessor='total_unit', verbose_name='Total Unit.')
    vat = tables.Column(accessor='vat', verbose_name='% IVA')
    vat_value = tables.Column(accessor='vat_value', verbose_name='IVA')
    discount = tables.Column(accessor='discount', verbose_name='% Desconto')
    discount_value = tables.Column(accessor='discount_value', verbose_name='Desconto')
    line_total = tables.Column(accessor='line_total', verbose_name='Total')

    class Meta:
        model = PurchasingOrderComponents
        attrs = {"class": "table"}
        fields = ('id', 'name', 'quantity', 'price_base', 'total_unit', 'vat', 'vat_value', 'discount', 'discount_value', 'line_total')
