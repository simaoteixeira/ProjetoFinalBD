from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.models import Warehouses
from projeto.tables.WarehousesTable import WarehousesTable


@login_required(login_url='/login')
def home(request):
    #table = WarehousesTable(Warehouses.objects.all())
    #table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        #'table': table,
        'navSection': 'inventario',
        'navSubSection': 'movimentos',
    }

    return render(request, 'movimentos/index.html', context)
