from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.repositories.StockMovmentsRepo import StockMovmentsRepo
from projeto.tables.StockMovmentsTable import StockMovmentsTable



@login_required(login_url='/login')
def home(request):
    table = StockMovmentsTable(StockMovmentsRepo().find_all())

    context = {
        'table': table,
        'navSection': 'inventario',
        'navSubSection': 'movimentos',
    }

    return render(request, 'movimentos/index.html', context)
