from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.forms.LaborsForm import LaborsForm
from projeto.repositories.LaborRepo import LaborRepo
from projeto.tables.LaborsTable import LaborsTable
from projeto.utils import getErrorsObject


@login_required(login_url='/login')
def home(request):
    table = LaborsTable(LaborRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'producao',
        'navSubSection': 'maoObra',
    }

    return render(request, 'maosObra/index.html', context)

@login_required(login_url='/login')
def create(request):
    form = LaborsForm(request.POST or None)

    context = {
        'form': form,
        'navSection': 'producao',
        'navSubSection': 'maoObra',
    }

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            LaborRepo().create(data['title'], data['cost'])

            return redirect('/producao/mao-obra')
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'maosObra/criar.html', context)