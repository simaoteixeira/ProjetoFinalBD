import django_tables2 as tables
from ..models import Labors

class ProductsTable(tables.Table):
    name = tables.Column(verbose_name="Nome", accessor="name")
    weight = tables.Column(verbose_name="Peso", accessor="weight")
    type = tables.Column(verbose_name="Tipo", accessor="type")
    price_base = tables.Column(verbose_name="Preço Base", accessor="price_base")

    class Meta:
        model = Labors
        attrs = {"class": "table"}
        fields = ("name", "weight", "type", "price_base")