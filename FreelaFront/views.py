import datetime
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView
from .services.sapf_connect import UserSession
from .services.tituloEleitoral_connect import ConsultaTituloEleitoral
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
import os
from .forms import LoginForm
from .services import cpfAPI_connect
from .services import  generatePdf
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate




class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/choice/'  # Redirecionar para a URL desejada após o sucesso

    def form_valid(self, form):
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
    url = reverse_lazy('home')
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ConsultaEleitoralView(View):
    def get(self, request):
        # Recupera variáveis da URL
        consulta_dados = request.session.get('consulta_dados', {})
        print(f"Eleitoral: {consulta_dados}")
        nome = consulta_dados.get('nome')
        nomeMae = consulta_dados.get('nomeMae')
        dataNascimento = consulta_dados.get('dataNascimento')

        if not all([nome, nomeMae, dataNascimento]):
            return HttpResponseBadRequest("Todos os parâmetros (nome, cpf, título eleitoral) são obrigatórios.")

        consultor = ConsultaTituloEleitoral('dPhltkwAeH77q-W9Qn5cstUB5vP6B7fOTfoplloa')
        consultor.execute(dataNascimento, nomeMae, nome)
        dados_logados = request.session.get('user_data',{})
        print(dados_logados)
        self.resultado = {'nome': nome,
                     'cpf': consulta_dados.get('cpf'),
                     'nTitulo': consultor.dados_recuperados['nTitulo'],
                     'zona': consultor.dados_recuperados['zona']}
        pdf_path = self.pdf_generate()
        # pdf_path = self.pdf_generate()
        with open(pdf_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="some_filename.pdf"'
            return response

    def pdf_generate(self, ):



        dados = {'nome': self.resultado['nome'],
                 'data_d': datetime.date.today().day,
                 'data_m': datetime.date.today().month,
                 'data_a': datetime.date.today().year,
                 'titulo': self.resultado['nTitulo'],
                 'zona': self.resultado['zona'],
                 'titulo_coletor': 'n logado no SAPF',
                 'nome_coletor': 'nome logado no SAPF'}
        # dados = {'nome': 'Geraldo Pereira De Castro Junior', 'data1': '22', 'data2': '33', 'data3': '4444',
        #  'titulo': '025239362089', 'zona': 'DF 005'}

        print(f"pdf daodos {dados}")
        input_pdf_path = os.path.join(settings.MEDIA_ROOT, '', 'ficha_apoio.pdf')
        output_pdf_path = os.path.join(settings.MEDIA_ROOT, f'pdfs/{dados["titulo_coletor"]}')
        os.makedirs(output_pdf_path, exist_ok=True)
        out_file = generatePdf.fill_form(input_pdf_path, dados, output_pdf_path + f'/{dados["titulo"]}.pdf')
        return out_file
class ConsultaCitizenView(View):
    def post(self, request, *args, **kwargs):
        cpf = request.POST.get('cpf', '')

        session = cpfAPI_connect.cpf_apiSession()
        request.session['consulta_dados'] = session.consultar_cpf(cpf)
        # session['consulta_dados'] = dados

        return HttpResponseRedirect(reverse('consulta_eleitoral'))

    def get(self, request, *args, **kwargs):
        return render(request, 'base/base.html')

def reg(requests):
    return render(requests, 'registration/login.html')


