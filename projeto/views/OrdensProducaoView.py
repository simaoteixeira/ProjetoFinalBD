from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.repositories.ProductionOrdersRepo import ProductionOrdersRepo
from projeto.tables.ProductionOrdersTable import ProductionOrdersTable


@login_required(login_url='/login')
def home(request):
    table = ProductionOrdersTable(ProductionOrdersRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'producao',
        'navSubSection': 'ordensProducao',
    }

    return render(request, 'ordensProducao/index.html', context)