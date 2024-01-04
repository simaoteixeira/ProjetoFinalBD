from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.enums.USERGROUPS import USERGROUPS
from projeto.forms.WarehousesForm import WarehousesForm
from projeto.repositories.WarehousesRepo import WarehousesRepo
from projeto.tables.WarehousesTable import WarehousesTable, WarehousesStockTable
from projeto.utils import permission_required, getErrorsObject


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.STOCK.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = WarehousesTable(WarehousesRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'inventario',
        'navSubSection': 'armazens',
    }

    return render(request, 'armazens/index.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.STOCK.value)
def view(request, id):
    userGroup = request.user.groups.all()[0].name

    repo = WarehousesRepo(
        connection=userGroup
    )
    data = repo.get_stock(id)

    if data is None:
        return render(request, '404.html', status=404)

    table = WarehousesStockTable(data)
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'n_armazem': id,
        'navSection': 'inventario',
        'navSubSection': 'armazens',
    }

    return render(request, 'armazens/armazem.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.STOCK.value)
def create(request):
    userGroup = request.user.groups.all()[0].name

    form = WarehousesForm(request.POST or None)

    context = {
        'form': form,
        'navSection': 'inventario',
        'navSubSection': 'armazens',
    }

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            WarehousesRepo(
                connection=userGroup
            ).create(data['name'], data['location'])

            return redirect('/inventario/armazens')
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'armazens/criar.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.STOCK.value)
def edit(request, id):
    userGroup = request.user.groups.all()[0].name

    repo = WarehousesRepo(
        connection=userGroup
    )
    data = repo.find_by_id(id)

    if data is None:
        return render(request, '404.html', status=404)

    form = WarehousesForm(request.POST or None, initial={
        'name': data.name,
        'location': data.location,
    })

    context = {
        'form': form,
        'edit': True,
        'navSection': 'inventario',
        'navSubSection': 'armazens',
    }

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            repo.update(id, data['name'], data['location'])

            return redirect('/inventario/armazens')
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'armazens/criar.html', context)
