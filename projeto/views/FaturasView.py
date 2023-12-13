from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.repositories.SupplierInvoicesRepo import SupplierInvoicesRepo
from projeto.tables.SupplierInvoicesTable import SupplierInvoicesTable


@login_required(login_url='/login')
def home(request):
    table = SupplierInvoicesTable(SupplierInvoicesRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'faturas',
    }

    return render(request, 'faturas/index.html', context)
