import django_tables2 as tables
from ..models import Suppliers


class SuppliersTable(tables.Table):
    name = tables.Column(verbose_name="Nome", accessor="name")
    nif = tables.Column(verbose_name="NIF", accessor="nif")
    phone = tables.Column(verbose_name="Telefone", accessor="phone")
    address = tables.Column(verbose_name="Morada", accessor="address")
    email = tables.Column(verbose_name="Email", accessor="email")

    class Meta:
        model = Suppliers
        attrs = {"class": "table"}
        fields = ("name", "nif", "phone", "address", "email")
