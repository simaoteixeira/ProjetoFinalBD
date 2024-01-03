from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from projeto.forms.ClientInvoicesForm import ClientInvoicesForm

from projeto.repositories.ClientInvoicesRepo import ClientInvoicesRepo
from projeto.repositories.ClientRepo import ClientRepo

from projeto.repositories.SalesOrdersRepo import SalesOrdersRepo
from projeto.tables.ClientInvoicesTable import ClientInvoicesTable
from projeto.tables.PurchasingOrdersTable import PurchasingOrdersProductsTable
from projeto.tables.SelectTables.SelectClientTable import SelectClientTable

from projeto.tables.SelectTables.SelectSalesOrdersTable import SelectSalesOrdersTable
from projeto.utils import getErrorsObject

@login_required(login_url='/login')
def home(request):
    table = ClientInvoicesTable(ClientInvoicesRepo().find_all())
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'table': table,
        'navSection': 'vendas',
        'navSubSection': 'faturasCliente',
    }

    return render(request, 'faturasCliente/index.html', context)


def create(request):
    clientRepo = ClientRepo()
    form = ClientInvoicesForm(request.POST or None)

    clients = clientRepo.find_all()

    clientsTable = SelectClientTable(clients)
    clientsTable.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'form': form,
        'clients': clients,
        'selectClientTable': clientsTable,
        'navSection': 'vendas',
        'navSubSection': 'faturasCliente',
    }

    if request.method == 'GET' and "selected_client" in request.GET or form['client'].value() is not None:
        selected_client = request.GET["selected_client"] or form.client.value
        salesOrdersRepo = SalesOrdersRepo()

        selected_client_name = ""

        for client in clients:
            if client.id_client == int(selected_client):
                selected_client_name = client.name
                break

        context["selected_client"] = selected_client_name
        context["selected_client_id"] = selected_client

        salesOrders = salesOrdersRepo.find_by_client(selected_client)
        salesOrdersTable = SelectSalesOrdersTable(salesOrders)

        context["salesOrders"] = salesOrders
        context["selectSalesOrdersTable"] = salesOrdersTable

        sales_orders = []

        for field in form.data:
            if (field.startswith("sales_order_")):
                if (form.data[field] is not None and form.data[field] != ""):
                    sales_orders.append(form.data[field])

        if len(sales_orders) > 0 and sales_orders[0] is not None:
            context["selected_sales_orders"] = sales_orders

            components = salesOrdersRepo.find_components_by_ids(sales_orders)
            context["components"] = components

    if request.method == 'POST':
        form = ClientInvoicesForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            ClientInvoicesRepo().create(
                data['client'],
                data['invoice_date'],
                data['expire_date'],
                data['obs'],
                data['products'],
                data['sales_orders']
            )

            return redirect('faturasCliente')
        else:
            errors = getErrorsObject(form.errors.get_context())

            context['errors'] = errors

    return render(request, 'faturasCliente/criar.html', context)

def view(request, id):
    repo = ClientInvoicesRepo()

    if request.method == 'POST' and request.POST.get('observations'):
        repo.update_obs(id, request.POST.get('observations'))

    data = repo.find_by_id(id)
    components = repo.find_components(id)

    componentsTable = PurchasingOrdersProductsTable(components)

    context = {
        'data': data,
        'componentsTable': componentsTable,
        'navSection': 'vendas',
        'navSubSection': 'faturasCliente',
    }

    if data is None:
        return render(request, '404.html', status=404)

    return render(request, 'faturasCliente/fatura.html', context)
