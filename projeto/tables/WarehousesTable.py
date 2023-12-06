import django_tables2 as tables
from ..models import Labors


class WarehousesTable(tables.Table):
    id = tables.Column(verbose_name="Codigo", accessor="id_warehouse")
    name = tables.Column(verbose_name="Nome", accessor="name")
    location = tables.Column(verbose_name="Localização", accessor="location")

    class Meta:
        model = Labors
        attrs = {"class": "table"}
        fields = ("id", "name", "location")