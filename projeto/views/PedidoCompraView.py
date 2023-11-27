from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.models import AuthUser
from projeto.tables.UsersTable import UsersTable


@login_required(login_url='/login')
def home(request):
    #model = AuthUser
    #table_class = UsersTable
    #template_name = 'django_tables2/tailwind.html'

    context = {
        'table': UsersTable(AuthUser.objects.all()),
        'navSection': 'compras',
        'navSubSection': 'pedidosCompra',
    }

    return render(request, 'pedidoCompra/index.html', context)
