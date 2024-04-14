from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .services.sapf_connect import UserSession
from .forms import LoginForm
from .services.cpfAPI_connect import cpf_apiSession
from django.views.decorators.csrf import csrf_exempt

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

    # Obtém o user_data da sessão, se existir
    user_data = request.session.get('user_data', {})

    # Renderiza o template de login, passando o formulário como contexto
    return render(request, 'login.html', {'form': form, 'user_data': user_data})

def logout_view(request):
    logout(request)
    return redirect('home')  # Substitua 'home' pelo nome da sua URL da página inicial


# Verifica se o usuário está autenticado antes de chamar a função pagina1

def choice(request):
    user_data = request.session.get('user_data', {})  # Obtém o user_data da sessão, se existir

    if request.method == 'POST':
        opcao = request.POST.get('opcao', None)
        if opcao == 'cpf':
            return render(request, 'base/base.html', {'user_data': user_data})
        elif opcao == 'nome':
            return render(request, 'area/nome.html', {'user_data': user_data})
    
    # Se não for um POST ou se a opção não for 'cpf' ou 'nome', renderiza 'area/choice.html' com user_data
    return render(request, 'area/choice.html', {'user_data': user_data})




# Verifica se o usuário está autenticado antes de chamar a função pagina1
@csrf_exempt
def test(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf', '')  # Obtém o CPF do formulário
        session = cpf_apiSession()  # Cria uma instância da sessão de API
        resultado = session.consultar_cpf(cpf)  # Faz a busca pelo CPF
        print(resultado)
        # Ajuste o caminho para o template aqui
        return render(request, 'area/resultado.html', {'resultado': resultado})
    else:
        print('n deu')
        # Corrija este caminho também se necessário
        return render(request, 'area/base.html')
    # print(f"Usuário autenticado: {request.user.is_authenticated}")
    # if request.method == 'POST':
    #     opc = request.POST.get('opc', None)
    #     if opc == 'Registrar Apoio':
    #         ver_cpf = request.POST.get('cpf', None)
    #         return HttpResponse(f'Sucesso! O cpf é: {ver_cpf}')
    #     else:
    #         return HttpResponse('Erro!')


    # Obtém o user_data da sessão, se existir
    user_data = request.session.get('user_data', {})
    return render(request, 'base/base.html', {'user_data': user_data})



def reg(requests):
    return render(requests, 'registration/login.html')

@csrf_exempt
def return_cpf (request):
    user_data = request.session.get('user_data', {}) 
    if request.method == 'POST':
        cpf = request.POST.get('cpf', '')  # Obtém o CPF do formulário
        session = cpf_apiSession()  # Cria uma instância da sessão de API
        resultado = session.consultar_cpf(cpf)  # Faz a busca pelo CPF
        print(resultado)
        # Ajuste o caminho para o template aqui
        return render(request, 'area/resultado.html', {'resultado': resultado, 'cpf': cpf, 'user_data': user_data})

