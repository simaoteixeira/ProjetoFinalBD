from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.enums.USERGROUPS import USERGROUPS
from projeto.forms.ClientOrdersForm import ClientOrdersForm
from projeto.forms.SalesOrdersForm import SalesOrdersForm
from projeto.repositories.ClientOrdersRepo import ClientOrdersRepo
from projeto.repositories.ClientRepo import ClientRepo
from projeto.repositories.SalesOrdersRepo import SalesOrdersRepo
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersProductsTable
from projeto.tables.SalesOrdersTable import SalesOrdersTable
from projeto.tables.SelectTables.SelectClientOrdersTable import SelectClientOrdersTable
from projeto.tables.SelectTables.SelectClientTable import SelectClientTable
from projeto.utils import getErrorsObject, permission_required


@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.VENDAS.value)
def home(request):
    userGroup = request.user.groups.all()[0].name

    table = SalesOrdersTable(SalesOrdersRepo(
        connection=userGroup
    ).find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'vendas',
        'navSubSection': 'guiasRemessa',
    }

    return render(request, 'guiasRemessa/index.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.VENDAS.value)
def create(request):
    userGroup = request.user.groups.all()[0].name

    clientRepo = ClientRepo(
        connection=userGroup
    )
    form = SalesOrdersForm(request.POST or None)

    clients = clientRepo.find_all()

    clientsTable = SelectClientTable(clients)
    clientsTable.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'form': form,
        'clients': clients,
        'selectClientTable': clientsTable,
        'navSection': 'vendas',
        'navSubSection': 'guiasRemessa',
    }

    if request.method == 'GET' and "selected_client" in request.GET or form['client'].value() is not None:
        selected_client = request.GET["selected_client"] or form.client.value
        clientOrdersRepo = ClientOrdersRepo(
            connection=userGroup
        )

        selected_client_name = ""

        for client in clients:
            if client.id_client == int(selected_client):
                selected_client_name = client.name
                break

        context["selected_client"] = selected_client_name
        context["selected_client_id"] = selected_client

        clientOrders = clientOrdersRepo.find_by_client(selected_client)
        clientOrdersTable = SelectClientOrdersTable(clientOrders)

        context["clientOrders"] = clientOrders
        context["selectClientOrdersTable"] = clientOrdersTable

        client_orders = []

        for field in form.data:
            if field.startswith("client_order_"):
                fieldData = form.data[field]

                if fieldData is not None and fieldData != "" and fieldData not in client_orders:
                    client_orders.append(fieldData)

        if len(client_orders) > 0 and client_orders[0] is not None:
            context["selected_client_orders"] = client_orders

            components = clientOrdersRepo.find_components_by_ids(client_orders)
            context["components"] = components

    if request.method == 'POST':
        form = SalesOrdersForm(request.POST)

        if ("submit" in form.data):
            if form.is_valid():
                data = form.cleaned_data

                SalesOrdersRepo(
                    connection=userGroup
                ).create(
                    id_user=request.user.id,
                    id_client_order=data["client_orders"],
                    obs=data["obs"],
                    products=data["products"],
                )

                return redirect('guiasRemessa')
            else:
                errors = getErrorsObject(form.errors.get_context())

                context['errors'] = errors

    return render(request, 'guiasRemessa/criar.html', context)

@login_required(login_url='/login')
@permission_required(USERGROUPS.ADMIN.value, USERGROUPS.VENDAS.value)
def view(request, id):
    userGroup = request.user.groups.all()[0].name

    repo = SalesOrdersRepo(
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
        'navSubSection': 'guiasRemessa',
    }

    if data is None:
        return render(request, '404.html', status=404)

    return render(request, 'guiasRemessa/guia.html', context)