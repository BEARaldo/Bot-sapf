import requests
from bs4 import BeautifulSoup

class user_session:
    def __init__(self):
        self.login_url = login_url = 'https://sapf.tse.jus.br/sapf/login'
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


        if ("severity:'error'" and "severityText:'Error'") not in response.text:
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                nome_completo = soup.find('p', {'class': 'menu-informacao-texto'}).get_text(strip=True)
                titulo_eleitoral = soup.find_all('p', {'class': 'menu-informacao-texto'})[1].get_text(strip=True)
                partido = soup.find_all('p', {'class': 'menu-informacao-texto'})[3].get_text(strip=True)

                self.user_data = {  # Dados do usuario logado
                    'name': nome_completo,
                    'titulo': titulo_eleitoral,
                    'partido': partido
                }
            except Exception as e:
                print(f"{'-'* 10}\nOcorreu erro:{e}\n{'-'* 10}")
            return True
        else:
            print("Login/Senha incorreta")
            return False

    def access_page(self, page_url):
        response = self.session.get(page_url, headers=self.headers)
        if response.ok:
            return response.text
        else:
            return None

# Teste da classe
if __name__ == '__main__':
    ##FUNCIONAL. Adaptar classe e funcionalidades em serviço que pode ser chamado dentro das views do Django
    user = user_session()
    # password = getpass.getpass(prompt='Password: ') #usando getpass #import getpass
    if user.login_user(input("Login:\n"), input("senha:\n")):
        # Teste da captura dos ddados de user
        for i in user.user_data:
            print(i)
        for key, value in user.user_data.items():
            print(f"{key}: {value}")
    else:
        print("Não foi possível fazer login")
        #fazer recursividade
