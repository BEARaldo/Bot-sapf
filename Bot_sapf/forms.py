from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import re

class LoginForm(forms.Form):
    titulo_eleitor = forms.CharField(required=True, max_length=12, min_length=12, label='Título de Eleitor')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    def clean(self):
        cleaned_data = super().clean()
        titulo_eleitor = cleaned_data.get('titulo_eleitor')
        password = cleaned_data.get('password')

        # Autenticar o usuário
        user = authenticate(username=titulo_eleitor, password=password)
        if not user:
            raise forms.ValidationError("Credenciais inválidas. Por favor, verifique o título de eleitor e a senha.")
        
        # Atualizar os dados com o usuário autenticado
        cleaned_data['user'] = user
        return cleaned_data

    def clean_titulo_eleitor(self):
        titulo_eleitor = self.cleaned_data.get('titulo_eleitor')

        # Valida se o título de eleitor segue o padrão esperado
        if not re.match(r'^\d{12}$', titulo_eleitor):
            raise forms.ValidationError("O título de eleitor deve conter 12 dígitos.")

        return titulo_eleitor


# forms.py
from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    nome_completo = forms.CharField(max_length=255)
    cpf = forms.CharField(max_length=14)
    titulo_eleitor = forms.CharField(max_length=12)
    nome_do_partido = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['titulo_eleitor', 'password']

