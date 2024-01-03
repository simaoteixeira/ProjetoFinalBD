from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.enums.USERGROUPS import USERGROUPS
from projeto.forms.ClientsForm import ClientsForm
from projeto.models import Clients
from projeto.repositories.ClientRepo import ClientRepo
from projeto.tables.ClientsTable import ClientsTable
from projeto.utils import getErrorsObject, permission_required


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.VENDAS.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = ClientsTable(ClientRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'vendas',
        'navSubSection': 'clientes',
    }

    return render(request, 'clientes/index.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.VENDAS.value)
def view(request, id):
    userGroup = request.user.groups.all()[0].name

    data = ClientRepo(
        connection=userGroup
    ).find_by_id(id)

    if data is None:
        return render(request, '404.html', status=404)

    context = {
        'data': data,
        'navSection': 'vendas',
        'navSubSection': 'clientes',
    }

    return render(request, 'clientes/cliente.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.VENDAS.value)
def create(request):
    userGroup = request.user.groups.all()[0].name

    repo = ClientRepo(
        connection=userGroup
    )
    form = ClientsForm(request.POST or None)

    context = {
        'form': form,
        'navSection': 'vendas',
        'navSubSection': 'clientes',
    }

    if request.method == 'POST':
        if form.is_valid():
            print('valid')
            print(form.cleaned_data)

            data = form.cleaned_data

            repo.create(data['name'], data['email'], data['nif'], data['phone'], data['address'], data['locality'], data['postal_code'])

            return redirect('/vendas/clientes')
        else:
            print('invalid')
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'clientes/criar.html', context)