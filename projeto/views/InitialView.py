from django.shortcuts import redirect

from projeto.enums.USERGROUPS import USERGROUPS


def home(request):
    userGroup = request.user.groups.all()[0].name

    #see user group and redirect to the correct page
    if userGroup == USERGROUPS.ADMIN.value:
        return redirect('home')
    elif userGroup == USERGROUPS.COMPRAS.value:
        return redirect('home')
    elif userGroup == USERGROUPS.STOCK.value:
        return redirect('inventario')
    elif userGroup == USERGROUPS.PRODUCAO.value:
        return redirect('producao')
    elif userGroup == USERGROUPS.VENDAS.value:
        return redirect('vendas')
    else:
        return redirect('login')