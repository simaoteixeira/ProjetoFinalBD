from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.forms.ProductionOrdersForm import ProductionOrdersForm
from projeto.repositories.ProductionOrdersRepo import ProductionOrdersRepo
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.tables.ProductionOrdersTable import ProductionOrdersTable
from projeto.tables.SelectTables.SelectProductsTable import SelectProductsTable


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

@login_required(login_url='/login')
def create(request):
    form = ProductionOrdersForm(request.POST or None)
    equipments = ProductsRepo().find_all_products()

    equipmentsTable = SelectProductsTable(equipments)

    context = {
        'form': form,
        'equipments': equipments,
        'selectEquipmentsTable': equipmentsTable,
        'navSection': 'producao',
        'navSubSection': 'ordensProducao',
    }