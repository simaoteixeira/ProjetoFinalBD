from django.urls import path
from .views import RegisterView, PedidoCompraView, FaturasView, FornecedoresView, RecessaoMaterialView

urlpatterns = [
    path('', PedidoCompraView.home, name='home'),
    path('compras', PedidoCompraView.home, name='home'),
    path('compras/faturas', FaturasView.home, name='home'),
    path('compras/fornecedores', FornecedoresView.home, name='home'),
    path('compras/recessao', RecessaoMaterialView.home, name='home'),
    path('registo', RegisterView.register, name='registo'),
]