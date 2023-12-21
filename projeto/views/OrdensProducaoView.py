from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.forms.ProductionOrdersForm import ProductionOrdersForm
from projeto.repositories.LaborRepo import LaborRepo
from projeto.repositories.ProductionOrdersRepo import ProductionOrdersRepo
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.repositories.WarehousesRepo import WarehousesRepo
from projeto.tables.ProductionOrdersTable import ProductionOrdersTable
from projeto.tables.SelectTables.SelectEquipmentsTable import SelectEquipmentsTable
from projeto.tables.SelectTables.SelectProductsTable import SelectProductsTable
from projeto.utils import getErrorsObject


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
    components = ProductsRepo().find_all_components()
    labors = LaborRepo().find_all()
    warehouses = WarehousesRepo().find_all()

    equipmentsTable = SelectEquipmentsTable(equipments)
    componentsTable = SelectProductsTable(components)

    context = {
        'form': form,
        'equipments': equipments,
        'selectEquipmentsTable': equipmentsTable,
        'components': components,
        'selectComponentsTable': componentsTable,
        'labors': labors,
        'warehouses': warehouses,
        'navSection': 'producao',
        'navSubSection': 'ordensProducao',
    }

    if request.method == 'GET' and "selected_equipment" in request.GET or form['product'].value() is not None:
        selected_equipment = request.GET["selected_equipment"] or form.product.value

        selected_equipment_name = ""

        for equipment in equipments:
            if equipment.id_product == int(selected_equipment):
                selected_equipment_name = equipment.name
                break

        context["selected_equipment"] = selected_equipment_name
        context["selected_equipment_id"] = selected_equipment

    if request.method == 'POST':
        form = ProductionOrdersForm(request.POST)
        data = form.data
        print(data)

        if form.is_valid():
            data = form.cleaned_data
            print(data)

            ProductionOrdersRepo().create(
                id_labor=data["labor"],
                id_user=request.user.id,
                id_product=data["product"],
                equipment_quantity=data["equipment_quantity"],
                obs=data["obs"],
                products=data["products"],
            )
        else:
            errors = getErrorsObject(form.errors.get_context())
            print(errors)

            context['errors'] = errors

    return render(request, 'ordensProducao/criar.html', context)
