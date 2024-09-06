from django.contrib.auth.models import User


username = input("Digite o usuario(titulo eleitoral) a se tornar admin: ")
user = User.objects.get(username)
if not user:
    print("Usuário não encontrado.\nCancelando...")


user.is_superuser = True
user.is_staff = True
user.save()

print(f"O usuário {user.username} agora é um superuser.")

------------------------------

from django.contrib.auth.models import User

# Substitua '123456789012' pelo nome de usuário que você deseja promover a superuser
user = User.objects.get(username='123456789012')

# Promover a superuser
user.is_superuser = True
user.is_staff = True
user.save()

print(f"O usuário {user.username} agora é um superuser.")
