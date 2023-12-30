import django_tables2 as tables

from projeto.models import ProductionOrders


class ProductionOrdersTable(tables.Table):
    product = tables.Column(verbose_name="Equipamento a produzir", accessor="product.name")
    quantity = tables.Column(verbose_name="Quantidade", accessor="equipment_quantity")
    production_cost = tables.Column(verbose_name="Custo de produção", accessor="production_cost")
    labor_cost = tables.Column(verbose_name="Mão de obra (€)", accessor="labor.cost")
    status = tables.Column(verbose_name="Estado", accessor="status")
    tools = tables.TemplateColumn(
        verbose_name="",
        template_name="core/_tools_column.html",
        orderable=False
    )

    class Meta:
        model = ProductionOrders
        attrs = {"class": "table"}
        fields = (
            "product",
            "quantity",
            "production_cost",
            "labor_cost",
            "status"
        )