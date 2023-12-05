from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.forms.ClientsForm import ClientsForm
from projeto.models import Clients
from projeto.tables.ClientsTable import ClientsTable
from projeto.utils import getErrorsObject


@login_required(login_url='/login')
def home(request):
    table = ClientsTable(Clients.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'vendas',
        'navSubSection': 'clientes',
    }

    return render(request, 'clientes/index.html', context)

@login_required(login_url='/login')
def create(request):
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

            return redirect('/vendas/clientes')
        else:
            print('invalid')
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'clientes/criar.html', context)