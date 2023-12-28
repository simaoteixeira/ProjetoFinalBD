from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.models import Warehouses
from projeto.repositories.WarehousesRepo import WarehousesRepo
from projeto.tables.WarehousesTable import WarehousesTable, WarehousesStockTable


@login_required(login_url='/login')
def home(request):
    table = WarehousesTable(WarehousesRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'inventario',
        'navSubSection': 'armazens',
    }

    return render(request, 'armazens/index.html', context)

def view(request, id):
    repo = WarehousesRepo()
    data = repo.get_stock(id)

    if data is None:
        return render(request, '404.html', status=404)

    table = WarehousesStockTable(repo.get_stock(id))
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'n_armazem': id,
        'navSection': 'inventario',
        'navSubSection': 'armazens',
    }

    return render(request, 'armazens/armazem.html', context)

