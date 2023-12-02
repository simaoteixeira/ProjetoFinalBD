from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.models import Clients
from projeto.tables.ClientsTable import ClientsTable


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
    if request.method == 'POST':
        client = Clients()
        client.name = request.POST.get('name')
        client.nif = request.POST.get('nif')
        client.address = request.POST.get('street')
        client.postal_code = request.POST.get('postal_code')
        client.locality = request.POST.get('city')
        client.phone = request.POST.get('phone')
        client.email = request.POST.get('email')
        #client.save()

        return redirect('/clientes')

    context = {
        'navSection': 'vendas',
        'navSubSection': 'clientes',
    }

    return render(request, 'clientes/criar.html', context)