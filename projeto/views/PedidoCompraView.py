from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.models import AuthUser
from projeto.repositories.PurchasingOrdersRepo import PurchasingOrdersRepo
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersTable
from projeto.tables.UsersTable import UsersTable


@login_required(login_url='/login')
def home(request):
    table = PurchasingOrdersTable(PurchasingOrdersRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'pedidosCompra',
    }

    return render(request, 'pedidoCompra/index.html', context)

@login_required(login_url='/login')
def view(request, id):
    context = {
        'navSection': 'compras',
        'navSubSection': 'pedidosCompra',
    }

    return render(request, 'pedidoCompra/pedido.html', context)

@login_required(login_url='/login')
def create(request):
    context = {
        'navSection': 'compras',
        'navSubSection': 'pedidosCompra',
    }

    return render(request, 'pedidoCompra/criar.html', context)