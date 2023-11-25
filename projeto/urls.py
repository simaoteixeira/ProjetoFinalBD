from django.urls import path
from .views import RegisterView, PedidoCompraView, FaturasView, FornecedoresView, RecessaoMaterialView

urlpatterns = [
    path('', PedidoCompraView.home, name='home'),
    path('compras', PedidoCompraView.home, name='home'),
    path('compras/faturas', FaturasView.home, name='faturas'),
    path('compras/fornecedores', FornecedoresView.home, name='fornecedores'),
    path('compras/recessao', RecessaoMaterialView.home, name='recessao'),
    path('registo', RegisterView.register, name='registo'),
]