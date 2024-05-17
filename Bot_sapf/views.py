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
from .services import sapf_connect, tituloEleitoral_connect, cpfAPI_connect, generatePdf
from .services.sapf_connect import UserSession
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/consultar_cpf/'  # Redirecionar para a URL desejada após o sucesso

    def form_valid(self, form):
        titulo_eleitor = form.cleaned_data['titulo_eleitor']
        password = form.cleaned_data['password']
        
        # Autenticar o usuário
        user = authenticate(username=titulo_eleitor, password=password)
        if user is not None:
            login(self.request, user)  # Login do usuário
            return super().form_valid(form)
        else:
            form.add_error(None, 'Seu título de eleitor ou senha está incorreto.')
            return self.form_invalid(form)


    def form_invalid(self, form):
        return super().form_invalid(form)


# views.py
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import UserRegistrationForm

class CadastrarView(FormView):
    template_name = 'cadastrar.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login_view')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


            
            

        return render(request, 'cadastrar.html')


class LogoutView(LoginRequiredMixin, RedirectView):
    

    url = reverse_lazy('login_view')
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
    

class ConsultaEleitoralView(View):
    async def get(self, request):
        import uuid
        # Recupera variáveis da URL
        consulta_dados = await sync_to_async(request.session.get)('consulta_dados', {})
        # print(f"Eleitoral: {consulta_dados}") #Verificar chegada dos dados
        nome = consulta_dados.get('Nome')
        nomeMae = consulta_dados.get('Nome da mãe')
        dataNascimento = consulta_dados.get('Nascimento')

        if not all([nome, nomeMae, dataNascimento]):
            return HttpResponseBadRequest(
                "Todos os parâmetros (nome, nome da mãe, data de nascimento) são obrigatórios.")

        # A linha seguinte deve ser ajustada para usar uma versão assíncrona da API ou biblioteca que você está utilizando
        consultor = tituloEleitoral_connect.ConsultaTituloEleitoral("t43krlWneEj99OBMvP3JCIfveSQY8fr4dI2HbZtM")
        self.dados_eleitorais = await sync_to_async(consultor.execute)(dataNascimento, nomeMae, nome)

        dados_logados = await sync_to_async(request.session.get)('user_data', {})
        print(dados_logados)

        self.resultado = {
            'nome': nome,
            'cpf': consulta_dados.get('cpf'),
            'nTitulo': self.dados_eleitorais['nTitulo'],
            'zona': self.dados_eleitorais['zona']
        }

        pdf_path = await sync_to_async(self.pdf_generate)()

        print(f'pdf path 1: {pdf_path}')
        if pdf_path:
            try:
                pdf_key = str(uuid.uuid4())  # Gerar um identificador único
                request.session['pdf_token'] = pdf_key
    
                request.session[pdf_key] = pdf_path  # Armazenar o caminho no objeto de sessão
                print(f'\n\ngerado session key: {pdf_key}\ncaminho pego com request.session.get(pdf_key,): {request.session.get(pdf_key,{})}\n\n')
                # return redirect('serve_pdf', pdf_key=pdf_key)
                return HttpResponseRedirect(reverse('serve_pdf', kwargs={'pdf_key': pdf_key}))
                # HttpResponseRedirect(request('./test_diretorio/pdf.html', {'pdf_url': pdf_url}))

                # return HttpResponseRedirect(request('./test_diretorio/pdf.html', {'pdf_key': pdf_key}))
    
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
    def pdf_generate(self, ):


        #titulotemporario
        self.titulo_consultor = 'n logado no SAPF'
        dados = {'nome': self.resultado['nome'],
                 'data_d': datetime.date.today().day,
                 'data_m': datetime.date.today().month,
                 'data_a': datetime.date.today().year,
                 'titulo': self.resultado['nTitulo'],
                 'zona': self.resultado['zona'],
                 'titulo_coletor': self.titulo_consultor,
                 'nome_coletor': 'nome logado no SAPF'}
        # dados = {'nome': 'Geraldo Pereira De Castro Junior', 'data1': '22', 'data2': '33', 'data3': '4444',
        #  'titulo': '025239362089', 'zona': 'DF 005'}

        print(f"pdf dados {dados}")
        input_pdf_path = os.path.join(settings.MEDIA_ROOT, 'ficha_apoio.pdf')

        output_pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', dados['titulo_coletor'])
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
        pdf_keyy = request.session.get('pdf_token')
        print('a',request.session.get(pdf_keyy,{}))
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
        return render(request, 'area/consultar_cpf.html')




