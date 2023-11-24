from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login')
def home(request):
    context = {
        'navSection': 'compras',
        'navSubSection': 'fornecedores',
    }

    return render(request, 'fornecedores/index.html', context)
