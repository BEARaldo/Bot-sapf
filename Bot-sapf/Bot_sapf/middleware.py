from django.shortcuts import redirect
from django.contrib import messages
from time import sleep

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith('/login/'):
            messages.warning(request, 'Você não está logado. Redirecionando...')
            response = redirect('login_view')
            response['X-Redirect-Delay'] = 1000  # Adiciona um cabeçalho para o tempo de atraso em milissegundos
            return response
        response = self.get_response(request)
        return response
