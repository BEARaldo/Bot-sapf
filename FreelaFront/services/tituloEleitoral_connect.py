import time

import requests


def converter_data_simples(data_string):
    dia, mes, ano = data_string.split('/')
    return f"{ano}-{mes}-{dia}"
class ConsultaTituloEleitoral:
    def __init__(self, token):
        self.url = 'https://api.infosimples.com/api/v2/consultas/tse/titulo'
        self.token = token
        self.timeout = 90
        self.dados_recuperados = None

    def execute(self, birthdate, mother, name):
        birthdate = converter_data_simples(birthdate)
        print(f"niver agora: {birthdate}")
        payload = {
            "birthdate": birthdate.lower(),
            "mother": mother.lower(),
            "name": name.lower(),
            "token": self.token,
            "timeout": self.timeout
        }

        print(f"Payload:\n{payload}")
        start_time = time.time()
        response = requests.post(self.url, payload)
        print(response.json())
        self.dados_recuperados = {'nome': name,
                                  'nTitulo' : response.json()['data'][0]['titulo_eleitoral'],
                                  'zona': response.json()['data'][0]['uf'] + ' ' + response.json()['data'][0]['zona']}

        print(f"Fim: {self.dados_recuperados}")
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        print(f"Tempo decorrido: {int(minutes)} minuto(s) e {int(seconds)} segundo(s).")
        response.close()

        return self.dados_recuperados


    def validate_response(self):
        if self.response_json is None:
            raise Exception("Consulta não foi executada.")

        if self.response_json['code'] == 200:
            return True
        return False

    def extract_details(self):
        if not self.validate_response():
            return None

        details_list = self.response_json['data']
        results = []

        for item in details_list:
            extracted = {
                'nome': item.get('nome', ''),
                'secao': item.get('secao', ''),
                'titulo_eleitoral': item.get('titulo_eleitoral', ''),
                'uf': item.get('uf', ''),
                'zona': item.get('zona', '')
            }
            results.append(extracted)

        return results


# # Uso da classe
# consulta = ConsultaTituloEleitoral(
#     token="tokken"
# )
#
# query = {'birthdate' : "1997-07-02",
# 'mother' : "cleonice maria de castro",
# 'name' : "geraldo pereira de castro junior"}
#
# consulta.execute(
#     query['birthdate'], query['mother'], query['name']
# )
#
# details = consulta.extract_details()
#
# if details is not None:
#     print("Detalhes extraídos:", details)
# else:
#     print("Falha ao extrair detalhes ou consulta não bem-sucedida.")
