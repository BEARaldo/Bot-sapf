from bs4 import BeautifulSoup


class UserSession:
    def __init__(self, requests):
        self.login_url = 'https://sapf.tse.jus.br/sapf/login'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }
        self.session = requests.Session()
        self.user_data = None

    def login_user(self, username, password):
        print(username, password)
        response = self.session.get(self.login_url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        view_state = soup.find('input', {'name': 'javax.faces.ViewState', 'id': 'j_id1:javax.faces.ViewState:0'})['value']

        payload = {
            'form': 'form',
            'username': username,
            'password': password,
            'entrar': 'Entrar',
            'javax.faces.ViewState': view_state
        }
        response = self.session.post(self.login_url, data=payload, headers=self.headers)

        if "severity:'error'" not in response.text and "severityText:'Error'" not in response.text:
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                nome_completo = soup.find('p', {'class': 'menu-informacao-texto'}).get_text(strip=True)
                titulo_eleitoral = soup.find_all('p', {'class': 'menu-informacao-texto'})[1].get_text(strip=True)
                partido = soup.find_all('p', {'class': 'menu-informacao-texto'})[3].get_text(strip=True)

                self.user_data = {  # Dados do usuário logado
                    'name': nome_completo,
                    'titulo': titulo_eleitoral,
                    'partido': partido
                }
                return True
            except Exception as e:
                print(f"{'-'* 10}\nOcorreu erro:{e}\n{'-'* 10}")
                return False
        else:
            return False

    def access_page(self, page_url, request):
        response = self.session.get(page_url, headers=self.headers)
        if response.ok:
            return response.text
        else:
            return None

# Teste da classe
# if __name__ == '__main__':
#     ##FUNCIONAL. Adaptar classe e funcionalidades em serviço que pode ser chamado dentro das views do Django
#     user = UserSession()
#     # password = getpass.getpass(prompt='Password: ') #usando getpass #import getpass
#     if user.login_user(input("Login:\n"), input("senha:\n")):
#         # Teste da captura dos dados de user
#         for i in user.user_data:
#             print(i)
#         for key, value in user.user_data.items():
#             print(f"{key}: {value}")
#     else:
#         print("Não foi possível fazer login")
#         #fazer recursividade
