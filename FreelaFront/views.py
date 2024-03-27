from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def home(requests):
    return render(requests, 'core/home.html')

@login_required
def login2(requests):
    return render(requests, 'registration/login.html')

@login_required
def pagina1(requests):
    return render(requests, 'core/pagina1.html')




