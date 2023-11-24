from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

from projeto.forms.RegisterForm import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/compras')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})