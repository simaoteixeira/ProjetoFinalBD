from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.enums.PRODUCTIONORDERSTATUS import PRODUCTIONORDERSTATUS
from projeto.enums.USERGROUPS import USERGROUPS
from projeto.forms.ProductionOrdersForm import ProductionOrdersForm
from projeto.repositories.LaborRepo import LaborRepo
from projeto.repositories.ProductionOrdersRepo import ProductionOrdersRepo
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.repositories.WarehousesRepo import WarehousesRepo
from projeto.tables.ProductionOrdersComponentsTable import ProductionOrdersComponentsTable
from projeto.tables.ProductionOrdersTable import ProductionOrdersTable
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersProductsTable
from projeto.tables.SelectTables.SelectEquipmentsTable import SelectEquipmentsTable
from projeto.tables.SelectTables.SelectProductsTable import SelectProductsTable
from projeto.utils import getErrorsObject, permission_required


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.PRODUCAO.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = ProductionOrdersTable(ProductionOrdersRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'producao',
        'navSubSection': 'ordensProducao',
    }

    return render(request, 'ordensProducao/index.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.PRODUCAO.value)
def view(request, id):
    userGroup = request.user.groups.all()[0].name

    repo = ProductionOrdersRepo(
        connection=userGroup
    )

    if request.method == 'GET' and request.GET.get('status'):
        status = request.GET.get('status')
        if status in PRODUCTIONORDERSTATUS:
            repo.update_status(id, status)

    if request.method == 'POST' and request.POST.get('observations'):
        repo.update_obs(id, request.POST.get('observations'))

    data = repo.find_by_id(id)
    components = repo.find_components(id)

    componentsTable = ProductionOrdersComponentsTable(components)

    context = {
        'data': data,
        'componentsTable': componentsTable,
        'navSection': 'producao',
        'navSubSection': 'ordensProducao',
    }

    return render(request, 'ordensProducao/ordemProducao.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.PRODUCAO.value)
def create(request):
    userGroup = request.user.groups.all()[0].name

    productsRepo = ProductsRepo(
        connection=userGroup
    )
    laborsRepo = LaborRepo(
        connection=userGroup
    )
    warehousesRepo = WarehousesRepo(
        connection=userGroup
    )
    form = ProductionOrdersForm(request.POST or None)

    equipments = productsRepo.find_all_products()
    components = productsRepo.find_all_components()
    labors = laborsRepo.find_all()
    warehouses = warehousesRepo.find_all()

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

        if form.is_valid():
            data = form.cleaned_data

            ProductionOrdersRepo(
                connection=userGroup
            ).create(
                id_labor=data["labor"],
                id_user=request.user.id,
                id_product=data["product"],
                equipment_quantity=data["equipment_quantity"],
                obs=data["obs"],
                products=data["products"],
            )

            return redirect("ordensProducao")
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'ordensProducao/criar.html', context)
