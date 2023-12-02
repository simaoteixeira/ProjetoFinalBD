from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.models import Suppliers
from projeto.tables.SuppliersTable import SuppliersTable


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
    if request.method == 'POST':
        supplier = Suppliers()
        supplier.name = request.POST.get('name')
        supplier.nif = request.POST.get('nif')
        supplier.address = request.POST.get('street')
        supplier.postal_code = request.POST.get('postal_code')
        supplier.locality = request.POST.get('city')
        supplier.phone = request.POST.get('phone')
        supplier.email = request.POST.get('email')
        #supplier.save()

        return redirect('/fornecedores')

    context = {
        'navSection': 'compras',
        'navSubSection': 'fornecedores',
    }

    return render(request, 'fornecedores/criar.html', context)