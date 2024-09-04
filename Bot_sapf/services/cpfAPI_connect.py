import requests
from bs4 import BeautifulSoup

class cpf_apiSession:
    def __init__(self):
        self.base_url = 'https://deskdata.com.br/pessoas/'
        self.cookie_manual = {
            'wordpress_logged_in_dd8782f26a34dfd3c646a09580a7757b': 'thihft%40gmail.com%7C1727889274%7ChmBePanfLUQXZkLPowAnRTNsC5ZHRlUHImbf5WAa7Ow%7C45dfdbd019adf63925c0ccdba4e7a9aa315f881534675de50c35f17c0877c382'
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
        print(response_post)
        self.dados = self.capturar_dados(response_post.text)

        ##DADOS TESTE##
        #self.dados = {'Nome': 'Geraldo PereirA', 'Gênero': 'Masculino', 'Nascimento': '02/002/1992', 'Idade': '22', 'CPF': '222.222.222-22', 'Situação do CPF': '2222222', 'Região fiscal': 'DF-GO-MS-MT-TO', 'Data de registro do CPF': '22/22/2022', 'Nome da mãe': 'MAE', 'Nome do pai': 'PAI', 'Nacionalidade': 'Brasileira', 'Signo': 'macho'}
        

        ##DADOS TESTE##
        print(f"Self dados é : {self.dados}")

        return self.dados
        
        if 'erros' not in response_post.text:
            self.dados = self.capturar_dados(response_post.text)
            print(f"Self dados é : {self.dados}")
            return self.dados
        else:
            return "Solicitação falhou. O CPF informado é inválido."




if __name__ == '__main__':
     client = cpf_apiSession()
     print(client.consultar_cpf(input("Digite o CPF:")))
