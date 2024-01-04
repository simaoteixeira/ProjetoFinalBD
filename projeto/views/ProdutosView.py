from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.enums.USERGROUPS import USERGROUPS
from projeto.forms.ProductForm import ProductForm
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.tables.ProductsTable import StockProductsTable, ProductsPerWarehouseTable, ProductsTable
from projeto.utils import getErrorsObject, permission_required


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.STOCK.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = ProductsTable(ProductsRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'inventario',
        'navSubSection': 'produtos',
    }

    return render(request, 'produtos/index.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.STOCK.value)
def create(request):
    userGroup = request.user.groups.all()[0].name

    form = ProductForm(request.POST or None)

    context = {
        'form': form,
        'navSection': 'inventario',
        'navSubSection': 'produtos',
    }

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            ProductsRepo(
                connection=userGroup
            ).create(
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

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.STOCK.value)
def view(request, id):
    userGroup = request.user.groups.all()[0].name

    repo = ProductsRepo(
        connection=userGroup
    )

    product = repo.find_by_id(id)

    if product is None:
        return render(request, '404.html', status=404)

    productsPerWarehouse = repo.find_product_stock_by_warehouse(id)

    productsPerWarehouseTable = ProductsPerWarehouseTable(productsPerWarehouse)

    context = {
        'product': product,
        'warehouseDistribution': productsPerWarehouseTable,
        'navSection': 'inventario',
        'navSubSection': 'produtos',
    }

    return render(request, 'produtos/produto.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.STOCK.value)
def edit(request, id):
    userGroup = request.user.groups.all()[0].name

    repo = ProductsRepo(
        connection=userGroup
    )

    product = repo.find_by_id(id)

    if product is None:
        return render(request, '404.html', status=404)

    form = ProductForm(request.POST or None, initial={
        'name': product.name,
        'type': product.type,
        'description': product.description,
        'weight': product.weight,
        'vat': product.vat,
        'profit_margin': product.profit_margin,
    })

    context = {
        'form': form,
        'edit': True,
        'navSection': 'inventario',
        'navSubSection': 'produtos',
    }

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            repo.edit(
                id_product=id,
                name=data['name'],
                description=data['description'],
                weight=data['weight'],
                vat=data['vat'],
                profit_margin=data['profit_margin'],
            )

            return redirect('/inventario/produtos')
        else:
            errors = getErrorsObject(form.errors.get_context())
            print(errors)

            context['errors'] = errors

    return render(request, 'produtos/criar.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.STOCK.value)
def import_products(request):
    userGroup = request.user.groups.all()[0].name

    if request.method == 'POST':
        file = request.FILES['product_data']

        if not file:
            return render(request, '404.html', status=404)

        if not file.name.endswith('.json'):
            return redirect('/inventario/produtos')

        ProductsRepo(
            connection=userGroup
        ).import_products(file.read().decode('utf-8'))

        return redirect('/inventario/produtos')

    return render(request, '404.html', status=404)