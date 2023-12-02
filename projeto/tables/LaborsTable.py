import django_tables2 as tables
from ..models import Labors


class LaborsTable(tables.Table):
    title = tables.Column(verbose_name="Designação", accessor="title")
    cost = tables.Column(verbose_name="Custo Base Serviço (€)", accessor="cost")

    class Meta:
        model = Labors
        attrs = {"class": "table"}
        fields = ("title", "cost")
