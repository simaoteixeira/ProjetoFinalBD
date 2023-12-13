from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projeto.repositories.MaterialReceiptsRepo import MaterialReceiptsRepo
from projeto.tables.MaterialReceiptsTable import MaterialReceiptsTable


@login_required(login_url='/login')
def home(request):
    table = MaterialReceiptsTable(MaterialReceiptsRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'compras',
        'navSubSection': 'rececaoMaterial',
    }

    return render(request, 'recessaoMaterial/index.html', context)
