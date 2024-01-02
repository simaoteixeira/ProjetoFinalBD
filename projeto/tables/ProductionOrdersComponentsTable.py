import django_tables2 as tables

from projeto.models import ProductionOrderComponents


class ProductionOrdersComponentsTable(tables.Table):
    quantity = tables.Column(accessor='quantity', verbose_name='Quantidade')
    name = tables.Column(accessor='product.name', verbose_name='Designação')
    price_base = tables.Column(accessor='price_base', verbose_name='Valor Unit.')

    class Meta:
        model = ProductionOrderComponents
        attrs = {"class": "table"}
        fields = (
            "quantity",
            "name",
            "price_base",
        )
