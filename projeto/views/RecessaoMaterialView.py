from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.forms.MaterialReceiptsForm import MaterialReceiptsForm
from projeto.repositories.MaterialReceiptsRepo import MaterialReceiptsRepo
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.repositories.PurchasingOrdersRepo import PurchasingOrdersRepo
from projeto.repositories.SupplierRepo import SupplierRepo
from projeto.repositories.WarehousesRepo import WarehousesRepo
from projeto.tables.MaterialReceiptsTable import MaterialReceiptsTable
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersProductsTable
from projeto.tables.SelectTables.SelectProductsTable import SelectProductsTable
from projeto.tables.SelectTables.SelectPurchasingOrdersTable import SelectPurchasingOrdersTable
from projeto.tables.SelectTables.SelectSupplierTable import SelectSupplierTable
from projeto.tables.SelectTables.SelectWarehousesTable import SelectWarehousesTable
from projeto.utils import getErrorsObject


@login_required(login_url='/login')
def home(request):
    table = MaterialReceiptsTable(MaterialReceiptsRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'rececaoMaterial',
    }

    return render(request, 'recessaoMaterial/index.html', context)

@login_required(login_url='/login')
def create(request):
    form = MaterialReceiptsForm(request.POST or None)
    suppliers = SupplierRepo().find_all()
    warehouses = WarehousesRepo().find_all()

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

        purchasingOrders = PurchasingOrdersRepo().find_by_supplier(selected_supplier)
        purchasingOrdersTable = SelectPurchasingOrdersTable(purchasingOrders)

        context["purchasingOrders"] = purchasingOrders
        context["selectPurchasingOrdersTable"] = purchasingOrdersTable

        if form['purchasing_order'].value() is not None:
            purchasingOrder = form['purchasing_order'].value()
            print("here", purchasingOrder)

            components = PurchasingOrdersRepo().find_components(purchasingOrder)
            componentsProducts = [{
                "id_product": component.product.id_product,
                "name": component.product.name,
                "quantity": component.quantity,
                "price_cost": component.total_unit,
                "vat": component.vat,
                "discount": component.discount,
            } for component in components]

            componentsTable = SelectProductsTable(componentsProducts)

            context["selectProductsTable"] = componentsTable

        if request.method == 'POST':
            form = MaterialReceiptsForm(request.POST)
            data = form.data
            print(data)
            if form.is_valid():
                data = form.cleaned_data
                print(data)

                MaterialReceiptsRepo().create(
                    request.user.id,
                    data['purchasing_order'],
                    data['n_delivery_note'],
                    data['obs'],
                    data['products']
                )

                return redirect('recessao')
            else:
                errors = getErrorsObject(form.errors.get_context())
                print(errors)

                context['errors'] = errors


    return render(request, 'recessaoMaterial/criar.html', context)

def view(request, id):
    if request.method == 'POST' and request.POST.get('observations'):
        MaterialReceiptsRepo().update_obs(id, request.POST.get('observations'))

    data = MaterialReceiptsRepo().find_by_id(id)
    components = MaterialReceiptsRepo().find_components(id)

    componentsTable = PurchasingOrdersProductsTable(components)

    print(data.total)

    context = {
        'data': data,
        'componentsTable': componentsTable,
        'navSection': 'compras',
        'navSubSection': 'rececaoMaterial',
    }

    if data is None:
        return render(request, '404.html', status=404)

    return render(request, 'recessaoMaterial/recessao.html', context)
