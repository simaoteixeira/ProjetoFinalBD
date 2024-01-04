from django.urls import path
from .views import RegisterView, PedidoCompraView, FaturasView, FornecedoresView, RecessaoMaterialView, ClientesView, \
    MaoObraView, ArmazensView, ProdutosView, MovimentosView, OrdensProducaoView, EncomendasClienteView, \
    GuiasRemessaView, FaturasClienteView, InitialView

urlpatterns = [
    path('', InitialView.home, name='home'),
    path('home', InitialView.home, name='home'),
    path('compras', PedidoCompraView.home, name='home'),

    path('compras/pedido/<slug:id>', PedidoCompraView.view, name='pedidoCompra'),
    path('compras/criar', PedidoCompraView.create, name='criarPedidoCompra'),
    path('compras/faturas', FaturasView.home, name='faturas'),
    path('compras/faturas/criar', FaturasView.create, name='criarFatura'),
    path('compras/faturas/<slug:id>', FaturasView.view, name='fatura'),
    path('compras/fornecedores', FornecedoresView.home, name='fornecedores'),
    path('compras/fornecedores/<int:id>', FornecedoresView.view, name='fornecedor'),
    path('compras/fornecedores/criar', FornecedoresView.create, name='criarFornecedor'),
    path('compras/fornecedores/<int:id>/editar', FornecedoresView.edit, name='editarFornecedor'),
    path('compras/recessao', RecessaoMaterialView.home, name='recessao'),
    path('compras/recessao/criar', RecessaoMaterialView.create, name='criarRecessao'),
    path('compras/recessao/<slug:id>', RecessaoMaterialView.view, name='recessaoMaterial'),

    path('vendas', EncomendasClienteView.home, name='vendas'),
    path('vendas/clientes', ClientesView.home, name='clientes'),
    path('vendas/clientes/<int:id>', ClientesView.view, name='cliente'),
    path('vendas/clientes/criar', ClientesView.create, name='criarCliente'),
    path('vendas/clientes/<int:id>/editar', ClientesView.edit, name='editarCliente'),
    path('vendas/encomendas', EncomendasClienteView.home, name='encomendasCliente'),
    path('vendas/encomendas/criar', EncomendasClienteView.create, name='criarEncomendaCliente'),
    path('vendas/encomendas/<int:id>', EncomendasClienteView.view, name='encomendaCliente'),
    path('vendas/guias-remessa', GuiasRemessaView.home, name='guiasRemessa'),
    path('vendas/guias-remessa/criar', GuiasRemessaView.create, name='criarGuiaRemessa'),
    path('vendas/guias-remessa/<slug:id>', GuiasRemessaView.view, name='guiaRemessa'),
    path('vendas/faturas', FaturasClienteView.home, name='faturasCliente'),
    path('vendas/faturas/criar', FaturasClienteView.create, name='criarFaturaCliente'),
    path('vendas/faturas/<slug:id>', FaturasClienteView.view, name='faturaCliente'),

    path('producao', OrdensProducaoView.home, name='producao'),
    path('producao/ordens-producao', OrdensProducaoView.home, name='ordensProducao'),
    path('producao/ordens-producao/<int:id>', OrdensProducaoView.view, name='ordemProducao'),
    path('producao/ordens-producao/criar', OrdensProducaoView.create, name='criarOrdemProducao'),
    path('producao/mao-obra', MaoObraView.home, name='maoObra'),
    path('producao/mao-obra/criar', MaoObraView.create, name='criarMaoObra'),

    path('inventario', MovimentosView.home, name='inventario'),
    path('inventario/movimentos', MovimentosView.home, name='movimentos'),
    path('inventario/armazens', ArmazensView.home, name='armazens'),
    path('inventario/armazens/<int:id>', ArmazensView.view, name='armazem'),
    path('inventario/produtos', ProdutosView.home, name='produtos'),
    path('inventario/produtos/criar', ProdutosView.create, name='criarProduto'),
    path('inventario/produtos/<int:id>', ProdutosView.view, name='produto'),
    path('inventario/produtos/<int:id>/editar', ProdutosView.edit, name='editarProduto'),

    path('registo', RegisterView.register, name='registo'),
]