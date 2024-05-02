from django import forms
import re


class LoginForm(forms.Form):
    titulo_eleitor = forms.CharField(required=True, max_length=12, min_length=12, label='Título de Eleitor')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    def clean_titulo_eleitor(self):
        titulo_eleitor = self.cleaned_data.get('titulo_eleitor')

        # Valida se o título de eleitor segue o padrão esperado
        if not re.match(r'^\d{12}$', titulo_eleitor):
            raise forms.ValidationError("O título de eleitor deve conter 12 dígitos.")

        return titulo_eleitor
