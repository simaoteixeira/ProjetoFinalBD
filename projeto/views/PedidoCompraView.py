from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.enums.USERGROUPS import USERGROUPS
from projeto.forms.PurchasingOrderForm import PurchasingOrdersForm
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.repositories.PurchasingOrdersRepo import PurchasingOrdersRepo
from projeto.repositories.SupplierRepo import SupplierRepo
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersTable, PurchasingOrdersProductsTable
from projeto.tables.SelectTables.SelectProductsTable import SelectProductsTable
from projeto.tables.SelectTables.SelectSupplierTable import SelectSupplierTable
from projeto.utils import getErrorsObject, permission_required


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.COMPRAS.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = PurchasingOrdersTable(PurchasingOrdersRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    print(request.user.groups.values_list('name', flat=True))

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'pedidosCompra',
    }

    return render(request, 'pedidoCompra/index.html', context)


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.COMPRAS.value)
def view(request, id):
    userGroup = request.user.groups.all()[0].name

    repo = PurchasingOrdersRepo(
        connection=userGroup
    )

    if request.method == 'POST' and request.POST.get('observations'):
        repo.update_obs(id, request.POST.get('observations'))

    data = repo.find_by_id(id)
    components = repo.find_components(id)

    componentsTable = PurchasingOrdersProductsTable(components)

    if data is None:
        return render(request, '404.html', status=404)

    context = {
        'data': data,
        'componentsTable': componentsTable,
        'navSection': 'compras',
        'navSubSection': 'pedidosCompra',
    }

    return render(request, 'pedidoCompra/pedido.html', context)


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.COMPRAS.value)
def create(request):
    userGroup = request.user.groups.all()[0].name

    supplierRepo = SupplierRepo(
        connection=userGroup
    )
    productsRepo = ProductsRepo(
        connection=userGroup
    )
    form = PurchasingOrdersForm(request.POST or None)

    suppliers = supplierRepo.find_all()
    components = productsRepo.find_all_components()

    suppliersTable = SelectSupplierTable(suppliers)
    suppliersTable.paginate(page=request.GET.get('page', 1), per_page=10)

    componentsTable = SelectProductsTable(components)

    context = {
        'form': form,
        'components': components,
        'selectComponentsTable': componentsTable,
        'suppliers': suppliers,
        'selectSupplierTable': suppliersTable,
        'navSection': 'compras',
        'navSubSection': 'pedidosCompra',
    }

    if request.method == 'GET' and "selected_supplier" in request.GET or form['supplier'].value() is not None:
        selected_supplier = request.GET["selected_supplier"] or form.supplier.value

        selected_supplier_name = ""

        for supplier in suppliers:
            if supplier.id_supplier == int(selected_supplier):
                selected_supplier_name = supplier.name
                break

        context["selected_supplier"] = selected_supplier_name
        context["selected_supplier_id"] = selected_supplier


    if request.method == 'POST':
        form = PurchasingOrdersForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            PurchasingOrdersRepo(
                connection=userGroup
            ).create(
                id_supplier=data["supplier"],
                id_user=request.user.id,
                delivery_date=data["date"],
                obs=data["obs"],
                products=data["products"]
            )

            return redirect('home')
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'pedidoCompra/criar.html', context)
