from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.forms.ProductForm import ProductForm
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.tables.ProductsTable import StockProductsTable, ProductsPerWarehouseTable, ProductsTable
from projeto.utils import getErrorsObject

@login_required(login_url='/login')
def home(request):
    table = ProductsTable(ProductsRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'inventario',
        'navSubSection': 'produtos',
    }

    return render(request, 'produtos/index.html', context)

@login_required(login_url='/login')
def create(request):
    form = ProductForm(request.POST or None)

    context = {
        'form': form,
        'navSection': 'inventario',
        'navSubSection': 'produtos',
    }

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            ProductsRepo().create(
                name=data['name'],
                type=data['type'],
                description=data['description'],
                weight=data['weight'],
                vat=data['vat'],
                profit_margin=data['profit_margin'],
            )

            return redirect('/inventario/produtos')
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'produtos/criar.html', context)

def view(request, id):
    repo = ProductsRepo()

    if request.method == 'POST' and request.POST.get('observations'):
        repo.update_obs(id, request.POST.get('observations'))

    product = repo.find_by_id(id)
    productsPerWarehouse = repo.find_product_stock_by_warehouse(id)

    productsPerWarehouseTable = ProductsPerWarehouseTable(productsPerWarehouse)

    context = {
        'product': product,
        'warehouseDistribution': productsPerWarehouseTable,
        'navSection': 'inventario',
        'navSubSection': 'produtos',
    }

    return render(request, 'produtos/produto.html', context)