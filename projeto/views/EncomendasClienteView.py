from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.enums.USERGROUPS import USERGROUPS
from projeto.forms.ClientOrdersForm import ClientOrdersForm
from projeto.repositories.ClientOrdersRepo import ClientOrdersRepo
from projeto.repositories.ClientRepo import ClientRepo
from projeto.repositories.ProductsRepo import ProductsRepo
from projeto.tables.ClientOrdersTable import ClientOrdersTable
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersProductsTable
from projeto.tables.SelectTables.SelectClientTable import SelectClientTable
from projeto.tables.SelectTables.SelectProductsTable import SelectProductsTable
from projeto.utils import getErrorsObject, permission_required


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.VENDAS.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = ClientOrdersTable(ClientOrdersRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'vendas',
        'navSubSection': 'encomendas',
    }

    return render(request, 'encomendasCliente/index.html', context)


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.VENDAS.value)
def create(request):
    userGroup = request.user.groups.all()[0].name

    clientsRepo = ClientRepo(
        connection=userGroup
    )
    productsRepo = ProductsRepo(
        connection=userGroup
    )
    form = ClientOrdersForm(request.POST or None)

    clients = clientsRepo.find_all()
    products = productsRepo.find_all()

    clientsTable = SelectClientTable(clients)

    productsTable = SelectProductsTable(products)

    context = {
        'form': form,
        'clients': clients,
        'components': products,
        'selectProductsTable': productsTable,
        'selectClientsTable': clientsTable,
        'navSection': 'vendas',
        'navSubSection': 'encomendas',
    }

    if request.method == 'GET' and "selected_client" in request.GET or form['client'].value() is not None:
        selected_client = request.GET["selected_client"] or form.client.value

        selected_client_name = ""

        for client in clients:
            if client.id_client == int(selected_client):
                selected_client_name = client.name
                break

        context["selected_client"] = selected_client_name
        context["selected_client_id"] = selected_client

    if request.method == 'POST':
        form = ClientOrdersForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            ClientOrdersRepo(
                connection=userGroup
            ).create(
                client=data["client"],
                obs=data["obs"],
                products=data["products"]
            )

            return redirect('encomendasCliente')

        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'encomendasCliente/criar.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.VENDAS.value)
def view(request, id):
    userGroup = request.user.groups.all()[0].name

    repo = ClientOrdersRepo(
        connection=userGroup
    )

    if request.method == 'POST' and request.POST.get('observations'):
        repo.update_obs(id, request.POST.get('observations'))

    data = repo.find_by_id(id)
    components = repo.find_components(id)

    componentsTable = PurchasingOrdersProductsTable(components)

    context = {
        'data': data,
        'componentsTable': componentsTable,
        'navSection': 'vendas',
        'navSubSection': 'encomendas',
    }

    if data is None:
        return render(request, '404.html', status=404)

    return render(request, 'encomendasCliente/encomenda.html', context)