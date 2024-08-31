import requests
from bs4 import BeautifulSoup

class cpf_apiSession:
    def __init__(self):
        self.base_url = 'https://deskdata.com.br/pessoas/'
        self.cookie_manual = {
            'wordpress_logged_in_dd8782f26a34dfd3c646a09580a7757b': 'thihft%40gmail.com%7C1716940020%7CE7FzL6b1Q9aCnRDKl3yb3gtri0TBHHQxYfVrg2PFvXU%7Cc2f39963e447996b2abdad79f7d6a0c62832d6f9ec6ec505680cb30df244116b'
        }
        self.dados = None

    def capturar_dados(self, html_response):
        soup = BeautifulSoup(html_response, 'html.parser')
        dados_basicos = {}
        tabela_dados_basicos = soup.find('table', class_='table-sm')
        if tabela_dados_basicos:
            linhas = tabela_dados_basicos.find_all('tr')
            for linha in linhas:
                rotulo = linha.find('th').text.strip()
                dado = linha.find('td').text.strip()
                dados_basicos[rotulo] = dado

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
        response_post = requests.post(self.base_url, data=payload_cpf, cookies=self.cookie_manual)
        if 'erros' not in response_post.text:
            self.dados = self.capturar_dados(response_post.text)
            return self.dados
        else:
            return "Solicitação falhou. O CPF informado é inválido."



# if __name__ == '__main__':
#     client = cpf_apiSession()
#     print(client.consultar_cpf(input("Digite o CPF:")))
