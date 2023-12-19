from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.models import AuthUser
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.repositories.PurchasingOrdersRepo import PurchasingOrdersRepo
from projeto.repositories.SupplierRepo import SupplierRepo
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersTable
from projeto.tables.SelectTables.SelectSupplierTable import SelectSupplierTable
from projeto.tables.UsersTable import UsersTable


@login_required(login_url='/login')
def home(request):
    table = PurchasingOrdersTable(PurchasingOrdersRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'pedidosCompra',
    }

    return render(request, 'pedidoCompra/index.html', context)


@login_required(login_url='/login')
def view(request, id):
    context = {
        'navSection': 'compras',
        'navSubSection': 'pedidosCompra',
    }

    return render(request, 'pedidoCompra/pedido.html', context)


@login_required(login_url='/login')
def create(request):
    suppliers = SupplierRepo().find_all()
    components = ProductsRepo().find_all_components()

    suppliersTable = SelectSupplierTable(suppliers)
    suppliersTable.paginate(page=request.GET.get('page', 1), per_page=10)

    #componentsTable =

    context = {
        'suppliers': suppliers,
        'selectSupplierTable': suppliersTable,
        'navSection': 'compras',
        'navSubSection': 'pedidosCompra',
    }

    if request.method == 'GET' and "selected_supplier" in request.GET:
        selected_supplier = request.GET["selected_supplier"]

        selected_supplier_name = ""

        for supplier in suppliers:
            if supplier.id_supplier == int(selected_supplier):
                selected_supplier_name = supplier.name
                break

        context["selected_supplier"] = selected_supplier_name

    return render(request, 'pedidoCompra/criar.html', context)
