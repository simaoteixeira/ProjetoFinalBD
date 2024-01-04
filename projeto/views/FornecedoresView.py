from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.enums.USERGROUPS import USERGROUPS
from projeto.forms.SuppliersForm import SuppliersForm
from projeto.models import Suppliers
from projeto.repositories.SupplierRepo import SupplierRepo
from projeto.tables.SuppliersTable import SuppliersTable
from projeto.utils import getErrorsObject, permission_required


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.COMPRAS.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = SuppliersTable(SupplierRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'fornecedores',
    }

    return render(request, 'fornecedores/index.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.COMPRAS.value)
def view(request, id):
    userGroup = request.user.groups.all()[0].name

    data = SupplierRepo(
        connection=userGroup
    ).find_by_id(id)

    if data is None:
        return render(request, '404.html', status=404)

    context = {
        'data': data,
        'supplierID': id,
        'navSection': 'compras',
        'navSubSection': 'fornecedores',
    }

    return render(request, 'fornecedores/fornecedor.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.COMPRAS.value)
def create(request):
    userGroup = request.user.groups.all()[0].name

    form = SuppliersForm(request.POST or None)

    context = {
        'form': form,
        'navSection': 'compras',
        'navSubSection': 'fornecedores',
    }

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            SupplierRepo(
                connection=userGroup
            ).create(data['name'], data['email'], data['nif'], data['phone'], data['address'], data['locality'], data['postal_code'])

            return redirect('/compras/fornecedores')
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'fornecedores/criar.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.COMPRAS.value)
def edit(request, id):
    userGroup = request.user.groups.all()[0].name

    repo = SupplierRepo(
        connection=userGroup
    )

    data = repo.find_by_id(id)

    if data is None:
        return render(request, '404.html', status=404)

    form = SuppliersForm(request.POST or None, initial={
        'name': data.name,
        'email': data.email,
        'nif': data.nif,
        'phone': data.phone,
        'address': data.address,
        'locality': data.locality,
        'postal_code': data.postal_code,
    })

    context = {
        'form': form,
        'edit': True,
        'navSection': 'compras',
        'navSubSection': 'fornecedores',
    }

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            repo.edit(id, data['name'], data['email'], data['nif'], data['phone'], data['address'], data['locality'], data['postal_code'])

            return redirect('/compras/fornecedores')
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'fornecedores/criar.html', context)