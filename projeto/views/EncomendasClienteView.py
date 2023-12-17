from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.repositories.ClientOrdersRepo import ClientOrdersRepo
from projeto.tables.ClientOrdersTable import ClientOrdersTable


@login_required(login_url='/login')
def home(request):
    table = ClientOrdersTable(ClientOrdersRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'vendas',
        'navSubSection': 'encomendas',
    }

    return render(request, 'encomendasCliente/index.html', context)