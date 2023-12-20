from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.forms.PurchasingOrderForm import PurchasingOrdersForm
from projeto.models import AuthUser
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.repositories.PurchasingOrdersRepo import PurchasingOrdersRepo
from projeto.repositories.SupplierRepo import SupplierRepo
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersTable
from projeto.tables.SelectTables.SelectProductsTable import SelectProductsTable
from projeto.tables.SelectTables.SelectSupplierTable import SelectSupplierTable
from projeto.tables.UsersTable import UsersTable
from projeto.utils import getErrorsObject


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
    form = PurchasingOrdersForm(request.POST or None)
    suppliers = SupplierRepo().find_all()
    components = ProductsRepo().find_all_components()

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
        data = form.data
        print(data)
        if form.is_valid():
            data = form.cleaned_data
            print(data)

            PurchasingOrdersRepo().create(
                id_supplier=data["supplier"],
                id_user=request.user.id,
                delivery_date=data["date"],
                obs=data["obs"],
                products=data["products"]
            )
        else:
            errors = getErrorsObject(form.errors.get_context())
            print(errors)

            context['errors'] = errors

    return render(request, 'pedidoCompra/criar.html', context)
