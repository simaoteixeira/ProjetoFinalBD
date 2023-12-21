import django_tables2 as tables

from projeto.models import ProductionOrders, StockMovements


class StockMovmentsTable(tables.Table):
    type = tables.Column(verbose_name="Tipo de Movimento", accessor="type")
    quantity = tables.Column(verbose_name="Quantidade", accessor="quantity")
    product = tables.Column(verbose_name="Componente/Equipamento", accessor="product.name")
    warehouse = tables.Column(verbose_name="Armazém", accessor="warehouse.name")
    prev_quantity = tables.Column(verbose_name="Stock Anterior", accessor="prev_quantity")
    pos_quantity = tables.Column(verbose_name="Stock Posterior", accessor="pos_quantity")
    reason = tables.Column(verbose_name="Motivo", accessor="reason")
    created_at = tables.Column(verbose_name="Data Movimento", accessor="created_at")

    class Meta:
        model = StockMovements
        attrs = {"class": "table"}
        fields = ["type", "quantity", "product", "warehouse", "prev_quantity", "pos_quantity", "created_at"]