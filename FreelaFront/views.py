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






class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/consultar_cpf/'  # Redirecionar para a URL desejada após o sucesso

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
    url = reverse_lazy('login_view')
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ConsultaEleitoralView(View):
    def get(self, request):
        # Recupera variáveis da URL
        consulta_dados = request.session.get('consulta_dados', {})
        print(f"Eleitoral: {consulta_dados}")
        nome = consulta_dados.get('Nome')
        nomeMae = consulta_dados.get('Nome da mãe')
        dataNascimento = consulta_dados.get('Nascimento')

        if not all([nome, nomeMae, dataNascimento]):
            return HttpResponseBadRequest("Todos os parâmetros (nome, cpf, título eleitoral) são obrigatórios.")

        consultor = ConsultaTituloEleitoral("VDRfLIYiiFqEy39v9fr6Q6c-1x4qyUTxzyhVdiIk")
        self.dados_eleitorais = consultor.execute(dataNascimento, nomeMae, nome)
        dados_logados = request.session.get('user_data',{})
        print(dados_logados)
        self.resultado = {'nome': nome,
                     'cpf': consulta_dados.get('cpf'),
                     'nTitulo': self.dados_eleitorais ['nTitulo'],
                     'zona': self.dados_eleitorais ['zona']}

        pdf_path = self.pdf_generate()
        pdf_path = pdf_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
        # with open(pdf_path, 'rb') as pdf:
        #     response = HttpResponse(pdf.read(), content_type='application/pdf')
        #     response['Content-Disposition'] = 'inline; filename="' + os.path.basename(pdf_path) + '"'
        #     return response

        return render(request, './test_diretorio/pdf.html', {'resultado': f"{self.resultado['nTitulo']}.pdf"})
    def pdf_load(self, ):
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'n logado no SAPF')

        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="' + os.path.basename(pdf_path) + self.resultado['nTitulo']
                return response
        else:
            return HttpResponseNotFound('The requested PDF was not found in our records.')
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

        print(f"pdf dados {dados}")
        input_pdf_path = os.path.join(settings.MEDIA_ROOT, '', 'ficha_apoio.pdf')
        output_pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs')
        os.makedirs(output_pdf_path, exist_ok=True)
        out_file = generatePdf.fill_form(input_pdf_path, dados, output_pdf_path + f'/{dados["titulo"]}.pdf')
        return out_file
class ServePDF(View):
    def get(self, request, filename):
        pdf_path = os.path.join(settings.MEDIA_ROOT,'pdfs',filename)
        print(pdf_path)
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="' + os.path.basename(pdf_path)
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




