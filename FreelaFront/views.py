from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .services.sapf_connect import UserSession
from .forms import LoginForm
from .services.cpfAPI_connect import cpf_apiSession
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .services.cpfAPI_connect import cpf_apiSession
from .services.test_infosimples import ConsultaTituloEleitoral
from datetime import datetime
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






# Verifica se o usuário está autenticado antes de chamar a função pagina1

def choice(request):
    user_data = request.session.get('user_data', {})  # Obtém o user_data da sessão, se existir
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
        return render(request, 'base/base.html', {'user_data': user_data})
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


def cpf_input_view(request):
        if request.method == 'POST':
            cpf = request.POST.get('cpf')
            print("CPF received:", cpf)  # Verifica se o CPF está sendo recebido
            if cpf:
                return combined_api_view(request, cpf)
            else:
                return render(request, 'area/input_form.html', {'error': 'CPF is required'})
        return render(request, 'area/input_form.html')

def combined_api_view(request,cpf):
        # cpf_session = cpf_apiSession(cpf)
        # personal_data = cpf_session.get_personal_data()

        # Utilize estes dados estáticos como alternativa para testes
        personal_data = {
            'Nome': 'geraldo pereira de castro junior',
            'Nascimento': '1997-07-02',
            'Nome da mãe': 'cleonice maria de castro'
        }

        if personal_data:
            # Função para formatar a data
            def format_date(date_str):
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    return date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    return date_str

            mapped_data = {
                'birthdate': format_date(personal_data.get('Nascimento')),
                'mother': personal_data.get('Nome da mãe'),
                'name': personal_data.get('Nome')
            }

            print("Sending the following data to ConsultaTituloEleitoral:")
            print(f"Name: {mapped_data['name']}")
            print(f"Mother's Name: {mapped_data['mother']}")
            print(f"Birthdate: {mapped_data['birthdate']}")

            consulta = ConsultaTituloEleitoral(
                token="TfOKDyyD-wrvUmN9o5yPzRq3rDGg_UiY4sJ8GRGg"
            )

            query = {'birthdate' : "1997-07-02",
            'mother' : "cleonice maria de castro",
            'name' : "geraldo pereira de castro junior"}

            consulta.execute(
                query['birthdate'], query['mother'], query['name']
            )

            details = consulta.extract_details()

            if details is not None:
                print("Detalhes extraídos:", details)
            else:
                print("Falha ao extrair detalhes ou consulta não bem-sucedida.")
            if details:
                print("Detalhes extraídos:", details)
                combined_data = {**mapped_data, **details}
                return JsonResponse(combined_data, safe=False)
            else:
                print("Falha ao extrair detalhes ou consulta não bem-sucedida.")
                return JsonResponse({"error": "Failed to retrieve electoral data"}, status=400)