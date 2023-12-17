from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.repositories.SalesOrdersRepo import SalesOrdersRepo
from projeto.tables.SalesOrdersTable import SalesOrdersTable


@login_required(login_url='/login')
def home(request):
    table = SalesOrdersTable(SalesOrdersRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'vendas',
        'navSubSection': 'guiasRemessa',
    }

    return render(request, 'encomendasCliente/index.html', context)