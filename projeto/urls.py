from django.urls import path
from .views import RegisterView, PedidoCompraView, FaturasView, FornecedoresView, RecessaoMaterialView, ClientesView, \
    MaoObraView

urlpatterns = [
    path('', PedidoCompraView.home, name='home'),
    path('home', PedidoCompraView.home, name='home'),
    path('compras', PedidoCompraView.home, name='home'),
    path('compras/pedido/<slug:id>', PedidoCompraView.view, name='pedidoCompra'),
    path('compras/criar', PedidoCompraView.create, name='criarPedidoCompra'),
    path('compras/faturas', FaturasView.home, name='faturas'),
    path('compras/fornecedores', FornecedoresView.home, name='fornecedores'),
    path('compras/fornecedores/criar', FornecedoresView.create, name='criarFornecedor'),
    path('compras/recessao', RecessaoMaterialView.home, name='recessao'),
    path('vendas/clientes', ClientesView.home, name='clientes'),
    path('vendas/clientes/criar', ClientesView.create, name='criarCliente'),
    path('producao/mao-obra', MaoObraView.home, name='maoObra'),
    path('producao/mao-obra/criar', MaoObraView.create, name='criarMaoObra'),
    path('registo', RegisterView.register, name='registo'),
]