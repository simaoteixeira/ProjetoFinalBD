import django_tables2 as tables
from ..models import PurchasingOrders


class PurchasingOrdersTable(tables.Table):
    Fornecedor = tables.Column(accessor='suppliers.name')
    #Componentes = tables.Column(accessor='purchasing_order_components.name')
    Valor = tables.Column(accessor='purchasing_orders.total_base')
    Delivery = tables.Column(accessor='purchasing_orders.delivery_date', verbose_name='Data Possivel de Entrega')
    RegistadoPor = tables.Column(accessor='auth_user.username', verbose_name='Registado por')
    Criado = tables.Column(accessor='purchasing_orders.created_at', verbose_name='Data de Criação Pedido')

    class Meta:
        #model = PurchasingOrders
        attrs = {"class": "table"}
        #fields = ("id_supplier", "total_base", "id_user", "created_at")
