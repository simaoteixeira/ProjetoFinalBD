from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.models import Labors
from projeto.tables.LaborsTable import LaborsTable


@login_required(login_url='/login')
def home(request):
    table = LaborsTable(Labors.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'producao',
        'navSubSection': 'maoObra',
    }

    return render(request, 'maosObra/index.html', context)

@login_required(login_url='/login')
def create(request):
    if request.method == 'POST':
        labor = Labors()
        labor.title = request.POST.get('title')
        labor.cost  = request.POST.get('cost')
        #labor.save()

        return redirect('/mao-obra')

    context = {
        'navSection': 'producao',
        'navSubSection': 'maoObra',
    }

    return render(request, 'maosObra/criar.html', context)