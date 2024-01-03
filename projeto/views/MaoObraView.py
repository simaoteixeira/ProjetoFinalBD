from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.enums.USERGROUPS import USERGROUPS
from projeto.forms.LaborsForm import LaborsForm
from projeto.repositories.LaborRepo import LaborRepo
from projeto.tables.LaborsTable import LaborsTable
from projeto.utils import getErrorsObject, permission_required


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.PRODUCAO.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = LaborsTable(LaborRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'producao',
        'navSubSection': 'maoObra',
    }

    return render(request, 'maosObra/index.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.PRODUCAO.value)
def create(request):
    userGroup = request.user.groups.all()[0].name

    form = LaborsForm(request.POST or None)

    context = {
        'form': form,
        'navSection': 'producao',
        'navSubSection': 'maoObra',
    }

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            LaborRepo(
                connection=userGroup
            ).create(data['title'], data['cost'])

            return redirect('/producao/mao-obra')
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'maosObra/criar.html', context)