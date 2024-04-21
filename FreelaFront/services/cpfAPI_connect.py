import requests
from bs4 import BeautifulSoup

class cpf_apiSession:
    def __init__(self):
        self.base_url = 'https://deskdata.com.br/pessoas/'
        self.cookie_manual = {
            'wordpress_logged_in_dd8782f26a34dfd3c646a09580a7757b': 'thihft%40gmail.com%7C1713780026%7Cndq1j1f1cltUZQcJsBU295xW2G3MOxUO1U0Eolk9FWu%7C139d26a84406f74f1e4c4e3ea50efe95880c829c8f9f427a681bb636784ccd8a'
        } # colocar em json ou variavel de sistema
        self.dados = None

    def capturar_dados(self, html_response):
        # soup = BeautifulSoup(html_response, 'html.parser')
        dados_basicos = {}
        # tabela_dados_basicos = soup.find('table', class_='table-sm')
        # if tabela_dados_basicos:
        #     linhas = tabela_dados_basicos.find_all('tr')
        #     for linha in linhas:
        #         rotulo = linha.find('th').text.strip()
        #         dado = linha.find('td').text.strip()
        #         dados_basicos[rotulo] = dado
        dados_basicos ={'nome': 'Geraldo Pereira De Castro Junior', 'dataNascimento': '02/07/1997', 'nomeMae': 'Cleonice Maria De Castro', 'cpf': '056.900.451-95'}

        return dados_basicos

    def consultar_cpf(self, cpf):
        payload_cpf = {
            "key-select": "cpf",
            "cpf": cpf,
            "key-extra-select": "",
            "basic_data": "basic_data",
            "search_type": "people",
            "submit": "Consultar",
            "duplicate-query-confirm": "false"
        }
        # response_post = requests.post(self.base_url, data=payload_cpf, cookies=self.cookie_manual)

        # if 'erros' not in response_post.text:
        #     dados = self.dados(response_post.text)
        self.dados = {'nome': 'Geraldo Pereira De Castro Junior', 'dataNascimento': '02/07/1997', 'nomeMae': 'Cleonice Maria De Castro', 'cpf': '056.900.451-95'}
        return self.dados
        # else:
        #     return "Solicitação falhou. O CPF informado é invalido."

# if __name__ == '__main__':
#     client = cpf_apiSession()
#     print(client.consultar_cpf(input("Digite o CPF:")))
