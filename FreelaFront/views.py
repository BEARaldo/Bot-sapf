from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .services.sapf_connect import UserSession
from .forms import LoginForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


#
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Cria uma instância do LoginForm com os dados enviados
        if form.is_valid():
            # Extrai o título de eleitor e senha validados do formulário
            titulo_eleitor = form.cleaned_data['titulo_eleitor']
            password = form.cleaned_data['password']

            # Utiliza os dados validados para tentar fazer o login
            user_session = UserSession()
            if user_session.login_user(titulo_eleitor, password):
                # Armazena informações do usuário na sessão do Django, se necessário
                request.session['user_data'] = user_session.user_data
                return redirect('choice')  # Redireciona para a página inicial após o login bem-sucedido
            else:
                # Se os dados de login não forem válidos, adiciona uma mensagem de erro
                messages.error(request, 'Usuário ou senha incorretos')
        else:
            # Se o formulário não for válido, mantém o usuário na página de login e mostra erros de validação
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        # Se não for uma requisição POST, exibe o formulário de login vazio
        form = LoginForm()

    # Renderiza o template de login, passando o formulário como contexto
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Substitua 'home' pelo nome da sua URL da página inicial


# Verifica se o usuário está autenticado antes de chamar a função pagina1
@login_required
def choice(requests):
    if requests.method == 'POST':
        opcao = requests.POST.get('opcao', None)
        if opcao == 'cpf':
            return render(requests, 'base/base.html')
        elif opcao == 'nome':
            return render(requests, 'area/nome.html')
    return render(requests, 'area/choice.html')



# Verifica se o usuário está autenticado antes de chamar a função pagina1
@login_required
def test(request):
    if request.method == 'POST':
        opc = request.POST.get('opc', None)
        if opc == 'Registrar Apoio':
            ver_cpf = request.POST.get('cpf', None)
            return HttpResponse(f'Sucesso! O cpf é: {ver_cpf}')
        else:
            return HttpResponse('Erro!')
    return render(request, 'base/base.html')


def reg(requests):
    return render(requests, 'registration/login.html')

