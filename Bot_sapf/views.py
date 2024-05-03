import datetime
import os
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, RedirectView, View, TemplateView
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from asgiref.sync import sync_to_async
import asyncio
from django.contrib.auth import logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings

from .forms import LoginForm
from .services import sapf_connect, tituloEleitoral_connect, cpfAPI_connect, generatePdf
from .services.sapf_connect import UserSession


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/consultar_cpf/'  # Redirecionar para a URL desejada após o sucesso

    def form_valid(self, form, request):
        titulo_eleitor = form.cleaned_data['titulo_eleitor']
        password = form.cleaned_data['password']
        user_session = UserSession()
        if user_session.login_user(titulo_eleitor, password):
            request.session['user_data'] = user_session.user_data
            return super().form_valid(form)
        else:
            form.add_error(None, 'Seu título de eleitor ou senha está incorreto.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class LogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('login_view')
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class ConsultaEleitoralView(View):
    async def get(self, request):
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

        # Aqui você decide como deseja tratar o retorno do PDF ou outro resultado
        return render(request, './test_diretorio/pdf.html', {'resultado': f"pdfs/{self.titulo_consultor}/{self.resultado['nTitulo']}.pdf"})

    def pdf_load(self, ):
        pdf_path = os.path.join(settings.MEDIA_ROOT, '')

        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="' + os.path.basename(pdf_path) + self.resultado['nTitulo']
                return response
        else:
            return HttpResponseNotFound('The requested PDF was not found in our records.')
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
        return out_file
class ServePDF(View):
    def get(self, request, filename):
        pdf_path = os.path.join(settings.MEDIA_ROOT,filename)
        print('no serve',pdf_path)
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="' + os.path.basename(pdf_path)
                #imprima response

                return response
        else:
            return HttpResponseNotFound('The requested PDF was not found in our records.')
class ConsultaCitizenView(View):
    def post(self, request, *args, **kwargs):
        cpf = request.POST.get('cpf', '')

        session = cpfAPI_connect.cpf_apiSession()
        request.session['consulta_dados'] = session.consultar_cpf(cpf)
        # session['consulta_dados'] = dados

        return HttpResponseRedirect(reverse('consulta_eleitoral'))

    def get(self, request, *args, **kwargs):
        return render(request, 'area/consultar_cpf.html')




