from django.urls import path
from .views import RegisterView, PedidoCompraView

urlpatterns = [
    path('', PedidoCompraView.home, name='home'),
    path('home', PedidoCompraView.home, name='home'),
    path('registo', RegisterView.register, name='registo'),
]