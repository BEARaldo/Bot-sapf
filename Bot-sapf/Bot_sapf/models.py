from django.db import models
from django.contrib.auth.models import User

class Cadastrados(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    titulo_eleitor = models.CharField(max_length=12)
    nome_do_partido = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_completo
