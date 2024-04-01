import requests
from bs4 import BeautifulSoup

class user_session:
    def __init__(self, login_url):
        self.login_url = login_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }
        self.session = requests.Session()

    def login_user(self, username, password):
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

        response = self.session.post(self.login_url, data=payload, headers=self.headers) #realiza o logon
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            nome_completo = soup.find('p', {'class': 'menu-informacao-texto'}).get_text(strip=True)
            titulo_eleitoral = soup.find_all('p', {'class': 'menu-informacao-texto'})[1].get_text(strip=True)

            self.user_data = {  # Dados do usuario logado
                'name': nome_completo,
                'titulo': titulo_eleitoral
            }
            return True
        else:
            return False

    def access_page(self, page_url):
        response = self.session.get(page_url, headers=self.headers)
        if response.ok:
            return response.text
        else:
            return None

# Teste da classe
##Colocar em json
login_url = 'https://sapf.tse.jus.br/sapf/login'
username = 'user'
password = 'senha'
#
user = user_session(login_url)
if user.login_user(username, password):
    # Teste da captura dos ddados de user
    print(user.user_data)
    # Teste de acesso a pagina - 1
    page_content = user.access_page('https://sapf.tse.jus.br/sapf/paginas/principal')
    print(page_content)

    # Teste de acesso a pagina - 2
    page_content = user.access_page('https://sapf.tse.jus.br/sapf/paginas/apoiamento/Consultar')#<- Pagina desejada
    print(page_content)
else:
    print("Não foi possível fazer login")
