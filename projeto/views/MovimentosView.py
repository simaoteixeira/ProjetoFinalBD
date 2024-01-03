from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.enums.USERGROUPS import USERGROUPS
from projeto.repositories.StockMovmentsRepo import StockMovmentsRepo
from projeto.tables.StockMovmentsTable import StockMovmentsTable
from projeto.utils import permission_required


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.STOCK.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = StockMovmentsTable(StockMovmentsRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'inventario',
        'navSubSection': 'movimentos',
    }

    return render(request, 'movimentos/index.html', context)
