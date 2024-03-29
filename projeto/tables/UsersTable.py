import django_tables2 as tables
from ..models import AuthUser


class UsersTable(tables.Table):
    class Meta:
        model = AuthUser
        attrs = {"class": "table"}
        fields = ("username", "email", "is_active", "date_joined")
