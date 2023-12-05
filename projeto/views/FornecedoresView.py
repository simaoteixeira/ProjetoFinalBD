from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.forms.SuppliersForm import SuppliersForm
from projeto.models import Suppliers
from projeto.tables.SuppliersTable import SuppliersTable
from projeto.utils import getErrorsObject


@login_required(login_url='/login')
def home(request):
    table = SuppliersTable(Suppliers.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'fornecedores',
    }

    return render(request, 'fornecedores/index.html', context)


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
            print('valid')
            print(form.cleaned_data)

            return redirect('/compras/fornecedores')
        else:
            print('invalid')
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'fornecedores/criar.html', context)
