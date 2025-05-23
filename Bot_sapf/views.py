import datetime
import os

from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, RedirectView, View, TemplateView
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, HttpResponseNotFound, FileResponse
from asgiref.sync import sync_to_async
import asyncio
from django.contrib.auth import logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from .forms import LoginForm
from .services import tituloEleitoral_connect, cpfAPI_connect, generatePdf
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Cadastrados 



logger = logging.getLogger(__name__)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/consultar_cpf/' 
    
    def form_valid(self, form):
        user = form.cleaned_data['user']
        login(self.request, user)
        
        return super().form_valid(form)
    
    
    def form_invalid(self, form):
        return super().form_invalid(form)

# --------------- VIEWS DE LOGIN ANTIGA ---------------
    # def form_valid(self, form):pyt
    #     titulo_eleitor = form.cleaned_data['titulo_eleitor']
    #     password = form.cleaned_data['password']
        
    #     # Autenticar o usuário
    #     user = authenticate(username=titulo_eleitor, password=password)
    #     if user is not None:
    #         login(self.request, user)  # Login do usuário
    #         return super().form_valid(form)
    #     else:
    #         form.add_error(None, 'Seu título de eleitor ou senha está incorreto.')
    #         return self.form_invalid(form)


    # def form_invalid(self, form):
    #     return super().form_invalid(form)
# --------------- VIEWS DE LOGIN ANTIGA ---------------




from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Cadastrados
from .forms import UserRegistrationForm

class CadastrarView(FormView):
    template_name = 'cadastrar.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login_view')

    def form_valid(self, form):
        nome_completo = form.cleaned_data['nome_completo']
        titulo_eleitor = form.cleaned_data['titulo_eleitor']
        cpf = form.cleaned_data['cpf']
        nome_do_partido = "Partido Desenvolvimento Sustentável"
        is_superuser = form.cleaned_data.get('is_superuser', False)
        password = form.cleaned_data['password']

        # Verificar se o usuário já existe com o título de eleitor fornecido
        # if User.objects.filter(username=titulo_eleitor).exists():
        #     return HttpResponse('Usuário já cadastrado')

        # Criar e salvar o usuário no modelo User do Django
        user_django = User.objects.create_user(username=titulo_eleitor, password=password)
        
        
        user_django.is_superuser = is_superuser
        user_django.is_staff = is_superuser  # Se for superusuário, também deve ser staff
        user_django.save()


        
        # Criar e salvar o usuário no modelo Cadastrados
        user = Cadastrados.objects.create(
            user=user_django,  # Associar o usuário Django ao modelo Cadastrados
            nome_completo=nome_completo,
            titulo_eleitor=titulo_eleitor,
            cpf=cpf,
            nome_do_partido=nome_do_partido,
        )
        user.save()

        return super(CadastrarView, self).form_valid(form)

            
            

        return render(request, 'cadastrar.html')
    
    def form_invalid(self, form):
        return super().form_invalid(form)


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cadastrados




class LogoutView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        print("Iniciando o processo de logout...")
        logout(request)  # Efetua o logout do usuário
        print("Logout realizado com sucesso.")
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        url = reverse_lazy('login_view')
        print(f"Redirecionando para: {url}")
        return url

class ConsultaEleitoralView(View):
    async def get(self, request):
        import uuid
        # Recupera variáveis da URL
        print("consultando o deskdata.")
        consulta_dados = await sync_to_async(request.session.get)('consulta_dados', {})
        print(f"Eleitoral: {consulta_dados}") #Verificar chegada dos dados deskdata
        #user_dados = await sync_to_async(request.session.get)('usuario', {})
        #print(f"usuario: {consulta_dados}") #Verificar chegada dos dados usuario


        self.nomelogado = request.session.get('usuario')
        self.tituloLogado = request.session.get('titulo_logado')
        print("Nome fazendo requisição:", self.nomelogado,'\ntitulo:',self.tituloLogado)

        nome = consulta_dados.get('Nome')
        nomeMae = consulta_dados.get('Nome da mãe')
        dataNascimento = consulta_dados.get('Nascimento')

        if not all([nome, nomeMae, dataNascimento]):
            return HttpResponseBadRequest(
                "Todos os parâmetros (nome, nome da mãe, data de nascimento) são obrigatórios.")
        infosimples = settings.INFOSIMPLES
        # A linha seguinte deve ser ajustada para usar uma versão assíncrona da API ou biblioteca que você está utilizando
        consultor = tituloEleitoral_connect.ConsultaTituloEleitoral(infosimples)
        self.dados_eleitorais = await sync_to_async(consultor.execute)(dataNascimento, nomeMae, nome)

        print('Retornou infosimples')

        self.resultado = {
            'nome': nome,
            'cpf': consulta_dados.get('cpf'),
            'nTitulo': self.dados_eleitorais['nTitulo'],
            'zona': self.dados_eleitorais['zona']
        }

        pdf_path = await sync_to_async(self.pdf_generate)()

        print(f'pdf path 1: {pdf_path}')
        if pdf_path:
            print('entrei no if')
            try:
                pdf_key = str(uuid.uuid4())  # Gerar um identificador único
                request.session['pdf_token'] = pdf_key
    
                request.session[pdf_key] = pdf_path  # Armazenar o caminho no objeto de sessão
                print(f'\n\ngerado session key: {pdf_key}\ncaminho pego com request.session.get(pdf_key,): {request.session.get(pdf_key,{})}\n\n')
                #return redirect('serve_pdf', pdf_key=pdf_key)
                #return HttpResponseRedirect(reverse('serve_pdf', kwargs={'pdf_key': pdf_key}))
                #HttpResponseRedirect(request('./test_diretorio/pdf.html', {'pdf_url': pdf_url}))
                return render(request, './test_diretorio/pdf.html', {'resultado': f"pdfs/{self.nomelogado}/{self.resultado['nTitulo']}.pdf"})
                return HttpResponseRedirect(request('./test_diretorio/pdf.html', {'pdf_key': pdf_key}))
    
            except Exception as e:
                HttpResponseNotFound({f'erro no negocio uuid:{e}'})
        else:
            return HttpResponseNotFound(request('./test_diretorio/pdf.html', {'pdf_key': 'Falha ao carregar arquivo. tente novamente'}))
        # Aqui você decide como deseja tratar o retorno do PDF ou outro resultado
        # return render(request, './test_diretorio/pdf.html', {'resultado': f"pdfs/{self.titulo_consultor}/{self.resultado['nTitulo']}.pdf"})
    # #########
    # def pdf_load(self, ):
    #     pdf_path = os.path.join(settings.MEDIA_ROOT, '')
    #
    #     if os.path.exists(pdf_path):
    #         with open(pdf_path, 'rb') as pdf:
    #             response = HttpResponse(pdf.read(), content_type='application/pdf')
    #             response['Content-Disposition'] = 'inline; filename="' + os.path.basename(pdf_path) + self.resultado['nTitulo']
    #             return response
    #     else:
    #         return HttpResponseNotFound('The requested PDF was not found in our records.')
############
    def pdf_generate(self):


        #AQUI É ONDE ESTÁ DANDO ERRO NBA CONSULTA DOS DADOS
        #print("CHEGUEI NO ERRO La")
        #titulo = request.session.get('titulo_eleitor')
        print("Título de eleitor salvo na sessão:", self.nomelogado,"\n",self.tituloLogado)
        #print("Oi", titulo)

        #self.titulo_consultor = request.session.get('titulo_eleitor')
        #self.nome_completo = request.session.get('nome_completo')
        dados = {'nome': self.resultado['nome'],
                 'data_d': datetime.date.today().day,
                 'data_m': datetime.date.today().month,
                 'data_a': datetime.date.today().year,
                 'titulo': self.resultado['nTitulo'],
                 'zona': self.resultado['zona'],
                 'titulo_coletor': self.tituloLogado,
                 'nome_coletor': self.nomelogado}
        # dados = {'nome': 'Geraldo Pereira De Castro Junior', 'data1': '22', 'data2': '33', 'data3': '4444',
        #  'titulo': '025239362089', 'zona': 'DF 005'}

        print(f"pdf dados {dados}")
        input_pdf_path = os.path.join(settings.MEDIA_ROOT, 'ficha_apoio.pdf')

        output_pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', dados['nome_coletor'])
        os.makedirs(output_pdf_path, exist_ok=True)
        out_file = generatePdf.fill_form(input_pdf_path, dados, output_pdf_path + f'/{dados["titulo"]}.pdf')
        print(f"arquivo salvo {out_file}")
        return out_file

class pdf_loadPage(View):
    def get(self,request,pdf_key):
        try:
            print(f'session key no servePDF: {type(pdf_key)}')
        except Exception as e:
            print(e)

        pdf_path = request.session.get(str(pdf_key))
        #pdf_keyy = request.session.get('pdf_token') #  TESTE
        #print('a',request.session.get(pdf_keyy,{}))
        print(f'pdfpath no servePDF: {pdf_path}')

        if pdf_path and os.path.exists(pdf_path):
            pdf_url = settings.MEDIA_URL + os.path.relpath(pdf_path, settings.MEDIA_ROOT)
            print(pdf_url)
            # return HttpResponseRedirect(reverse('serve_pdf', kwargs={'pdf_key': pdf_key}))
            return render(request, './test_diretorio/pdf.html', {'pdf_key': pdf_key})


        else:
            return HttpResponseNotFound('Erro na consulta do PDF. Arquivo não encontrado')
        # if pdf_path and os.path.exists(pdf_path):
        #     with open(pdf_path, 'rb') as pdf:
        #         response = HttpResponse(pdf.read(), content_type='application/pdf')
        #         response['Content-Disposition'] = 'inline; filename="' + os.path.basename(pdf_path)
        #         return response

        logger.debug(f"Session Key: {pdf_key}")
        logger.debug(f"PDF Path from session: {pdf_path}")

        if pdf_path and os.path.exists(pdf_path):
            pdf_url = settings.MEDIA_URL + os.path.relpath(pdf_path, settings.MEDIA_ROOT)
            print(pdf_url)
            # return HttpResponseRedirect(reverse('serve_pdf', kwargs={'pdf_key': pdf_key}))
            return render(request, './test_diretorio/pdf.html', {'pdf_key': pdf_key})


class ServePDF(View):

    def get(self, request, pdf_key):
        pdf_path = request.session.get(str(pdf_key))#se pa str() é necessário
        print('f',pdf_path)
        if pdf_path and os.path.exists(pdf_path):
            try:
                return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
            except Exception as e:
                return HttpResponseNotFound('Error loading the PDF: {}'.format(e))
        else:
            return HttpResponseNotFound('The requested PDF was not found.')

# def get(self, request, pdf_key):
        # try:
        #     print(f'session key no servePDF: {type(pdf_key)}')
        # except Exception as e:
        #     print(e)
        #
        # pdf_path = request.session.get(str(pdf_key))
        # pdf_keyy = request.session.get('pdf_token')
        # print(request.session.get(pdf_keyy,{}))
        # print(f'pdfpath no servePDF: {pdf_path}')
        #
        # if pdf_path and os.path.exists(pdf_path):
        #     with open(pdf_path, 'rb') as pdf:
        #         response = HttpResponse(pdf.read(), content_type='application/pdf')
        #         response['Content-Disposition'] = 'inline; filename="' + os.path.basename(pdf_path)
        #         return response
        # else:
        #     return HttpResponseNotFound('Erro na consulta do PDF. Arquivo não encontrado')

        # logger.debug(f"Session Key: {pdf_key}")
        # logger.debug(f"PDF Path from session: {pdf_path}")

        # if pdf_path and os.path.exists(pdf_path):
        #     pdf_url = settings.MEDIA_URL + os.path.relpath(pdf_path, settings.MEDIA_ROOT)
        #     print(pdf_url)
        #     # return HttpResponseRedirect(reverse('serve_pdf', kwargs={'pdf_key': pdf_key}))
        #     return render(request, './test_diretorio/pdf.html', {'pdf_key': pdf_key})



class ConsultaCitizenView(View):
    def post(self, request, *args, **kwargs):
        import uuid
        cpf = request.POST.get('cpf', '')

        session = cpfAPI_connect.cpf_apiSession()
        request.session['consulta_dados'] = session.consultar_cpf(cpf)
        # pdf_key = str(uuid.uuid4())  
        # request.session['pdf_token'] = pdf_key
        # request.session[pdf_keyy] = 'apareci'  # Armazenar o caminho no objeto de sessão
        # session['consulta_dados'] = dados

        return HttpResponseRedirect(reverse('consulta_eleitoral'))

    def get(self, request, *args, **kwargs):
        # Obtém o usuário atualmente autenticado da requisição
        user = request.user

        # Tenta recuperar o registro do usuário no modelo Cadastrados; 
        # lança um erro 404 se não for encontrado
        cadastrado = get_object_or_404(Cadastrados, user=user)

        request.session['usuario'] = cadastrado.nome_completo
        request.session['titulo_logado'] = cadastrado.titulo_eleitor

        print("Nome salvo na sessão:", request.session.get('usuario'),'\ntitulo:',request.session.get('titulo_logado'))

        # Prepara o contexto com as informações do usuário para renderizar no template
        context = {
            'nome_completo': cadastrado.nome_completo,  # Nome completo do usuário
            'titulo_eleitor': cadastrado.titulo_eleitor,  # Título de eleitor do usuário
            'cpf': cadastrado.cpf,  # CPF do usuário
            'nome_do_partido': cadastrado.nome_do_partido,  # Nome do partido associado ao usuário
        }
        


        # Renderiza o template 'consultar_cpf.html' com o contexto preenchido
        return render(request, 'area/consultar_cpf.html', context)



# @login_required
# def usuarios(request):
#     todos_usuarios = Cadastrados.objects.all()
#     todos_usuarios_django = User.objects.all()

#     # Combinar os QuerySets em uma única variável
#     todos_usuarios_combinados = chain(todos_usuarios, todos_usuarios_django)
    
    
#     return render(request, 'area/usuarios.html')
    