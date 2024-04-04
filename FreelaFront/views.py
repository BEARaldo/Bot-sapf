from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(requests):
    return render(requests, 'core/home.html')

#Verifica se o usuário está autenticado antes de chamar a função login2
@login_required
def login2(requests):
    return render(requests, 'registration/login.html')

#Verifica se o usuário está autenticado antes de chamar a função pagina1
@login_required
def pagina1(requests):
    return render(requests, 'core/pagina1.html')

#Verifica se o usuário está autenticado antes de chamar a função pagina1
@login_required
def choice(requests):
    if requests.method == 'POST':
        opcao = requests.POST.get('opcao', None)
        if opcao == 'cpf':
            return render(requests, 'base/base.html') 
        elif opcao == 'nome':
            return render(requests, 'area/nome.html') 
    return render(requests, 'area/choice.html')

#Verifica se o usuário está autenticado antes de chamar a função pagina1
@login_required
def test(requests):
    return render(requests, 'base/base.html')


def reg(requests):
    return render(requests, 'registration/login.html')