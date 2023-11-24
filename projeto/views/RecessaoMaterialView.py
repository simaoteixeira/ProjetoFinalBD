from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login')
def home(request):
    context = {
        'navSection': 'compras',
        'navSubSection': 'rececaoMaterial',
    }

    return render(request, 'recessaoMaterial/index.html', context)
