import django_tables2 as tables
from ..models import PurchasingOrders


class PurchasingOrdersTable(tables.Table):
    supplier = tables.Column(accessor='supplier.name', verbose_name='Fornecedor')
    total = tables.Column(accessor='total', verbose_name='Valor')
    delivery_date = tables.Column(accessor='delivery_date', verbose_name='Data Possivel de entrega')
    user = tables.Column(accessor='user.username', verbose_name='Registado por')
    created_at = tables.Column(accessor='created_at', verbose_name='Data de Criação do Pedido')

    class Meta:
        model = PurchasingOrders
        attrs = {"class": "table"}
        fields = ('supplier', 'total', 'delivery_date', 'user', 'created_at')