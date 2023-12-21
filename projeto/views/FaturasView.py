from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.forms.SupplierInvoicesForm import SupplierInvoicesForm
from projeto.repositories.MaterialReceiptsRepo import MaterialReceiptsRepo
from projeto.repositories.SupplierInvoicesRepo import SupplierInvoicesRepo
from projeto.repositories.SupplierRepo import SupplierRepo
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersProductsTable
from projeto.tables.SelectTables.SelectMaterialReceiptsTable import SelectMaterialReceiptsTable
from projeto.tables.SelectTables.SelectSupplierTable import SelectSupplierTable
from projeto.tables.SupplierInvoicesTable import SupplierInvoicesTable
from projeto.utils import getErrorsObject


@login_required(login_url='/login')
def home(request):
    table = SupplierInvoicesTable(SupplierInvoicesRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'faturas',
    }

    return render(request, 'faturas/index.html', context)


def create(request):
    form = SupplierInvoicesForm(request.POST or None)
    suppliers = SupplierRepo().find_all()

    suppliersTable = SelectSupplierTable(suppliers)
    suppliersTable.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'form': form,
        'suppliers': suppliers,
        'selectSupplierTable': suppliersTable,
        'navSection': 'compras',
        'navSubSection': 'faturas',
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

        materialReceipts = MaterialReceiptsRepo().find_by_supplier(selected_supplier)
        materialReceiptsTable = SelectMaterialReceiptsTable(materialReceipts)

        context["materialReceipts"] = materialReceipts
        context["selectMaterialReceiptsTable"] = materialReceiptsTable

        material_receipts = []

        for field in form.data:
            if (field.startswith("material_receipt_")):
                if (form.data[field] is not None and form.data[field] != ""):
                    material_receipts.append(form.data[field])

        if len(material_receipts) > 0 and material_receipts[0] is not None:
            context["selected_material_receipts"] = material_receipts

            components = MaterialReceiptsRepo().find_components_by_ids(material_receipts)
            context["components"] = components

    if request.method == 'POST':
        form = SupplierInvoicesForm(request.POST)
        data = form.data
        print(data)

        if form.is_valid():
            data = form.cleaned_data
            print(data)

            SupplierInvoicesRepo().create(
                data['supplier'],
                data['invoice_id'],
                data['invoice_date'],
                data['expire_date'],
                data['obs'],
                data['products'],
                data['material_receipts']
            )

            #return redirect('faturas')
        else:
            errors = getErrorsObject(form.errors.get_context())
            print(errors)

            context['errors'] = errors

    return render(request, 'faturas/criar.html', context)

def view(request, id):
    if request.method == 'POST' and request.POST.get('observations'):
        SupplierInvoicesRepo().update_obs(id, request.POST.get('observations'))

    data = SupplierInvoicesRepo().find_by_id(id)
    components = SupplierInvoicesRepo().find_components(id)

    componentsTable = PurchasingOrdersProductsTable(components)

    context = {
        'data': data,
        'componentsTable': componentsTable,
        'navSection': 'compras',
        'navSubSection': 'faturas',
    }

    if data is None:
        return render(request, '404.html', status=404)

    print(data.material_receptions)

    return render(request, 'faturas/fatura.html', context)
