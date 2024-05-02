import datetime
import os
from django.shortcuts import render, redirect
from django.views.generic import FormView, View
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.contrib.auth import logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from .forms import LoginForm
from django.urls import reverse


from .services import cpfAPI_connect, generatePdf, tituloEleitoral_connect


class LoginView(FormView, View):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/consultar_cpf/'  # Redirecionar para a URL desejada após o sucesso

    def form_valid(self, form):
        titulo_eleitor = form.cleaned_data['titulo_eleitor']
        password = form.cleaned_data['password']
        usuario = authenticate(username=titulo_eleitor, password=password)

        if usuario is not None:
            return redirect('consultar_cpf')
        else:
            return redirect('login_view')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('login_view'))


class ConsultaEleitoralView(View):
    def get(self, request):
        consulta_dados = request.session.get('consulta_dados', {})
        nome = consulta_dados.get('Nome')
        nomeMae = consulta_dados.get('Nome da mãe')
        dataNascimento = consulta_dados.get('Nascimento')

        if not all([nome, nomeMae, dataNascimento]):
            return HttpResponseBadRequest("Todos os parâmetros (nome, cpf, título eleitoral) são obrigatórios.")

        consultor = tituloEleitoral_connect.ConsultaTituloEleitoral("VDRfLIYiiFqEy39v9fr6Q6c-1x4qyUTxzyhVdiIk")
        dados_eleitorais = consultor.execute(dataNascimento, nomeMae, nome)

        resultado = {
            'nome': nome,
            'cpf': consulta_dados.get('cpf'),
            'nTitulo': dados_eleitorais['nTitulo'],
            'zona': dados_eleitorais['zona']
        }

        pdf_path = self.pdf_generate(resultado)
        pdf_path = pdf_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)

        return render(request, './test_diretorio/pdf.html', {'resultado': f"{resultado['nTitulo']}.pdf"})

    def pdf_generate(self, resultado):
        dados = {
            'nome': resultado['nome'],
            'data_d': datetime.date.today().day,
            'data_m': datetime.date.today().month,
            'data_a': datetime.date.today().year,
            'titulo': resultado['nTitulo'],
            'zona': resultado['zona'],
            'titulo_coletor': 'n logado no SAPF',
            'nome_coletor': 'nome logado no SAPF'
        }

        input_pdf_path = os.path.join(settings.MEDIA_ROOT, '', 'ficha_apoio.pdf')
        output_pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs')
        os.makedirs(output_pdf_path, exist_ok=True)
        out_file = generatePdf.fill_form(input_pdf_path, dados, output_pdf_path + f'/{dados["titulo"]}.pdf')
        return out_file


class ServePDF(View):
    def get(self, request, filename):
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)

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

        return HttpResponseRedirect(reverse('consulta_eleitoral'))

    def get(self, request, *args, **kwargs):
        return render(request, 'area/consultar_cpf.html')
