from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.forms.SuppliersForm import SuppliersForm
from projeto.models import Suppliers
from projeto.repositories.SupplierRepo import SupplierRepo
from projeto.tables.SuppliersTable import SuppliersTable
from projeto.utils import getErrorsObject


@login_required(login_url='/login')
def home(request):
    table = SuppliersTable(SupplierRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'fornecedores',
    }

    return render(request, 'fornecedores/index.html', context)

@login_required(login_url='/login')
def view(request, id):
    data = SupplierRepo().find_by_id(id)

    if data is None:
        return render(request, '404.html', status=404)

    context = {
        'data': data,
        'navSection': 'compras',
        'navSubSection': 'fornecedores',
    }

    return render(request, 'fornecedores/fornecedor.html', context)

@login_required(login_url='/login')
def create(request):
    form = SuppliersForm(request.POST or None)

    context = {
        'form': form,
        'navSection': 'compras',
        'navSubSection': 'fornecedores',
    }

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            SupplierRepo().create(data['name'], data['email'], data['nif'], data['phone'], data['address'], data['locality'], data['postal_code'])

            return redirect('/compras/fornecedores')
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'fornecedores/criar.html', context)
