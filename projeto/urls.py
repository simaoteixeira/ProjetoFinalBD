from django.urls import path
from .views import HomeView, RegisterView

urlpatterns = [
    path('', HomeView.home, name='home'),
    path('home', HomeView.home, name='home'),
    path('registo', RegisterView.register, name='registo'),
]