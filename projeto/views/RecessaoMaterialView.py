from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.enums.USERGROUPS import USERGROUPS
from projeto.forms.MaterialReceiptsForm import MaterialReceiptsForm
from projeto.repositories.MaterialReceiptsRepo import MaterialReceiptsRepo
from projeto.repositories.PurchasingOrdersRepo import PurchasingOrdersRepo
from projeto.repositories.SupplierRepo import SupplierRepo
from projeto.repositories.WarehousesRepo import WarehousesRepo
from projeto.tables.MaterialReceiptsTable import MaterialReceiptsTable
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersProductsTable
from projeto.tables.SelectTables.SelectProductsTable import SelectProductsTable
from projeto.tables.SelectTables.SelectPurchasingOrdersTable import SelectPurchasingOrdersTable
from projeto.tables.SelectTables.SelectSupplierTable import SelectSupplierTable
from projeto.tables.SelectTables.SelectWarehousesTable import SelectWarehousesTable
from projeto.utils import getErrorsObject, permission_required


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.COMPRAS.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = MaterialReceiptsTable(MaterialReceiptsRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'rececaoMaterial',
    }

    return render(request, 'recessaoMaterial/index.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.COMPRAS.value)
def create(request):
    userGroup = request.user.groups.all()[0].name

    supplierRepo = SupplierRepo(
        connection=userGroup
    )
    warehousesRepo = WarehousesRepo(
        connection=userGroup
    )
    form = MaterialReceiptsForm(request.POST or None)

    suppliers = supplierRepo.find_all()
    warehouses = warehousesRepo.find_all()

    suppliersTable = SelectSupplierTable(suppliers)
    suppliersTable.paginate(page=request.GET.get('page', 1), per_page=10)

    warehousesTable = SelectWarehousesTable(warehouses)
    warehousesTable.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'form': form,
        'suppliers': suppliers,
        'selectSupplierTable': suppliersTable,
        'warehouses': warehouses,
        'selectWarehousesTable': warehousesTable,
        'navSection': 'compras',
        'navSubSection': 'rececaoMaterial',
    }

    if request.method == 'GET' and "selected_supplier" in request.GET or form['supplier'].value() is not None:
        selected_supplier = request.GET["selected_supplier"] or form.supplier.value
        purchasingOrderRepo = PurchasingOrdersRepo()

        selected_supplier_name = ""

        for supplier in suppliers:
            if supplier.id_supplier == int(selected_supplier):
                selected_supplier_name = supplier.name
                break

        context["selected_supplier"] = selected_supplier_name
        context["selected_supplier_id"] = selected_supplier

        purchasingOrders = purchasingOrderRepo.find_by_supplier(selected_supplier)
        purchasingOrdersTable = SelectPurchasingOrdersTable(purchasingOrders)

        context["purchasingOrders"] = purchasingOrders
        context["selectPurchasingOrdersTable"] = purchasingOrdersTable

        if form['purchasing_order'].value() is not None:
            purchasingOrder = form['purchasing_order'].value()

            components = purchasingOrderRepo.find_components(purchasingOrder)
            componentsProducts = [{
                "id_product": component.product.id_product,
                "name": component.product.name,
                "quantity": component.quantity,
                "price_cost": component.price_base,
                "vat": component.vat,
                "discount": component.discount,
            } for component in components]

            componentsTable = SelectProductsTable(componentsProducts)

            context["selectProductsTable"] = componentsTable

        if request.method == 'POST':
            form = MaterialReceiptsForm(request.POST)

            if form.is_valid():
                data = form.cleaned_data

                MaterialReceiptsRepo(
                    connection=userGroup
                ).create(
                    request.user.id,
                    data['purchasing_order'],
                    data['n_delivery_note'],
                    data['obs'],
                    data['products']
                )

                return redirect('recessao')
            else:
                errors = getErrorsObject(form.errors.get_context())

                context['errors'] = errors


    return render(request, 'recessaoMaterial/criar.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.COMPRAS.value)
def view(request, id):
    userGroup = request.user.groups.all()[0].name

    repo = MaterialReceiptsRepo(
        connection=userGroup
    )

    if request.method == 'POST' and request.POST.get('observations'):
        repo.update_obs(id, request.POST.get('observations'))

    data = repo.find_by_id(id)
    components = repo.find_components(id)

    componentsTable = PurchasingOrdersProductsTable(components)

    context = {
        'data': data,
        'componentsTable': componentsTable,
        'navSection': 'compras',
        'navSubSection': 'rececaoMaterial',
    }

    if data is None:
        return render(request, '404.html', status=404)

    return render(request, 'recessaoMaterial/recessao.html', context)
