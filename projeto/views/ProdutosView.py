from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.forms.ProductForm import ProductForm
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.tables.ProductsTable import StockProductsTable
from projeto.utils import getErrorsObject

@login_required(login_url='/login')
def home(request):
    table = StockProductsTable(ProductsRepo().find_all_stock())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'inventario',
        'navSubSection': 'produtos',
    }

    return render(request, 'produtos/index.html', context)

@login_required(login_url='/login')
def create(request):
    form = ProductForm(request.POST or None)

    context = {
        'form': form,
        'navSection': 'inventario',
        'navSubSection': 'produtos',
    }

    if request.method == 'POST':
        if form.is_valid():
            print('valid')
            print(form.cleaned_data)

            data = form.cleaned_data

            ProductsRepo().create(data)

            return redirect('/inventario/produtos')
        else:
            print('invalid')
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'produtos/criar.html', context)