from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import re

# Classe para o Login

class LoginForm(forms.Form):
    titulo_eleitor = forms.CharField(
        max_length=12,
        widget=forms.TextInput(
            attrs={
                'name': 'titulo_eleitor',
                'placeholder': 'Título de Eleitor',
                'id': 'Titueleitor',
            }
        )
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'name': 'password',
                'placeholder': 'Senha',
                'id': 'senha',
            }
        )
    )
    
    def clean(self):
        cleaned_data = super().clean()
        titulo_eleitor = cleaned_data.get('titulo_eleitor')
        password = cleaned_data.get('password')

        if titulo_eleitor and password:
            # Verifica se o título tem 12 caracteres
            if len(titulo_eleitor) != 12:
                self.add_error('titulo_eleitor', "O título de eleitor deve conter exatamente 12 dígitos")
                return cleaned_data
            
            # Verifica o título no banco de dados
            verifica_titulo = User.objects.filter(username=titulo_eleitor).first()
            if not verifica_titulo:
                self.add_error("titulo_eleitor", "Título de eleitor não cadastrado.")
                return cleaned_data
            
            # Autentica o usuário
            usuario_autenticado = authenticate(username=titulo_eleitor, password=password)
            # Verifica a senha
            if usuario_autenticado is None:
                self.add_error('password', "Credenciais inválidas. Por favor, verifique o título de eleitor e a senha.")
                return cleaned_data
            else:
                cleaned_data['user'] = usuario_autenticado

        return cleaned_data
                 
                 
# Classe para Cadastrar

class UserRegistrationForm(forms.ModelForm):
    nome_completo = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'name': 'nome_completo',
                'placeholder': 'Nome Completo',
                'id': 'nome',
            }
        )
    )
    
    cpf = forms.CharField(
        max_length=14,
        widget=forms.TextInput(
            attrs={
                'name': 'cpf',
                'placeholder': 'CPF',
                'id': 'cpf',
            }
        )
    )
    
    titulo_eleitor = forms.CharField(
        max_length=12,
        widget=forms.TextInput(
            attrs={
                'name': 'titulo_eleitor',
                'placeholder': 'Título de Eleitor',
                'id': 'Titueleitor',
            }
        )
    )
    is_superuser = forms.BooleanField(
        label='Super Administrador',
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'ver_senha'})
    )
    
    # nome_do_partido = forms.CharField(
    #     initial='Partido Desenvolvimento Sustentável',
    #     max_length=30,
    #     required=False,
    #     widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'campo-partido'})
    # )
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'name': 'password',
                'placeholder': 'Senha',
                'id': 'senha',
            }
        )
    )
    
    
    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome_completo')
        titulo_eleitor = cleaned_data.get('titulo_eleitor')
        cpf = cleaned_data.get('cpf')
        # nome_do_partido = cleaned_data.get('nome_do_partido')
        password = cleaned_data.get('password')
        
        if len(titulo_eleitor) != 12:
            self.add_error('titulo_eleitor', "O título de eleitor deve conter exatamente 12 dígitos")
            
        verifica_titulo = User.objects.filter(username=titulo_eleitor).exists()
        if verifica_titulo:
            self.add_error("titulo_eleitor", "Usuário já cadastrado.")
            return cleaned_data

            

    class Meta:
        model = User
        fields = ['titulo_eleitor', 'password', 'is_superuser']
        
        
        
class ProcurarForm(forms.Form):
    cpf = forms.CharField(
        max_length=14,
        widget=forms.TextInput(
            attrs={
                'name': 'cpf',
                'placeholder': 'CPF',
                'id': 'cpf',
            }
        )
    )






# ---------------- login antigo --------------------------

        # user = authenticate(username=titulo_eleitor, password=password)
        # if titulo_eleitor:
        #     user = authenticate(username=titulo_eleitor, password=password)
        #     if not user:
        #         try:
        #             user = User.objects.get(username=titulo_eleitor)
        #         except User.DoesNotExist:
        #             self.add_error('titulo_eleitor', "O título de eleitor informado está incorreto.")
        #             return cleaned_data

        #         if not user.check_password(password):
        #             self.add_error('password', "A senha informada está incorreta.")
        #             return cleaned_data

        # if not user:
        #     raise forms.ValidationError("Credenciais inválidas. Por favor, verifique o título de eleitor e a senha.")
        
        # cleaned_data['user'] = user
        # return cleaned_data

    # def clean_titulo_eleitor(self):
    #     titulo_eleitor = self.cleaned_data.get('titulo_eleitor')

    #     if not re.match(r'^\d{12}$', titulo_eleitor):
    #         raise forms.ValidationError("O título de eleitor deve conter 12 dígitos.")

    #     return titulo_eleitor

# ---------------- login antigo --------------------------