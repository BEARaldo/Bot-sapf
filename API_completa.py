import requests
from bs4 import BeautifulSoup

class ConsultaTituloEleitoral:
    # O código da classe ConsultaTituloEleitoral permanece inalterado, exceto pelo método extract_details.

    def extract_details(self):
        if not self.validate_response():
            return None

        details_list = self.response_json['data']
        results = []

        for item in details_list:
            extracted = {
                'nome': item.get('nome', ''),
                'titulo_eleitoral': item.get('titulo_eleitoral', ''),
                'zona': item.get('zona', '')  # Adicionando a zona eleitoral
            }
            results.append(extracted)

        return results

class cpf_apiSession:
    # O código da classe cpf_apiSession permanece inalterado, exceto no método consultar_cpf.

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
            dados = self.capturar_dados(response_post.text)

            # Consulta o título eleitoral
            consulta = ConsultaTituloEleitoral(token="tokken")  # Substitua "tokken" pelo seu token real
            consulta.execute(
                query['birthdate'], query['mother'], query['name']
            )
            details = consulta.extract_details()

            if details is not None:
                # Adiciona o título eleitoral e a zona eleitoral aos dados
                dados['Título Eleitoral'] = details[0]['titulo_eleitoral']
                dados['Zona Eleitoral'] = details[0]['zona']

            return dados
        else:
            return "Solicitação falhou. O CPF informado é inválido."

if __name__ == '__main__':
    client = cpf_apiSession()
    print(client.consultar_cpf(input("Digite o CPF:")))
