from django.contrib.auth.models import User


username = input("Digite o usuario(titulo eleitoral) a se tornar admin: ")
user = User.objects.get(username)
if not user:
    print("Usuário não encontrado.\nCancelando...")


user.is_superuser = True
user.is_staff = True
user.save()

print(f"O usuário {user.username} agora é um superuser.")
