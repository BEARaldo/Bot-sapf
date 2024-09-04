import requests
import time
# from dateutil import parser

def converter_data_simples(data_string):
    try:
        d,m,y = data_string.split('/')
        # return parser.parse(partes).strftime('%Y-%m-%d')
        return f'{y}-{m}-{d}'
    except ValueError as e:
        raise ValueError(f"Data fornecida '{data_string}' está em formato inválido ou é inválida. Detalhe: {e}")



class ConsultaTituloEleitoral:
    def __init__(self, token):
        self.session = requests.Session()
        self.url = 'https://api.infosimples.com/api/v2/consultas/tse/titulo'
        self.token = token
        self.timeout = 300  # Timeout inicial
        self.dados_recuperados = None
        self.response_json = None

    def execute(self, birthdate, mother, name):

        birthdate = converter_data_simples(birthdate)
        print(birthdate)

        payload = {
            "birthdate": birthdate.lower(),
            "mother": mother.lower(),
            "name": name.lower(),
            "token": self.token,
            # "timeout": self.timeout
        }
        max_attempts = 5
        backoff_factor = 3
        start_time = time.time()
        for attempt in range(max_attempts):
            try:
                payload['timeout'] = int(self.timeout)
                print(payload)
                return {'nome': name, 'nTitulo': '1231231123', 'zona': 'poteiro' + ' ' + '01/01/01'}
                #response = self.session.post(self.url, payload)
                data = response.json()
                if data['code'] != 200:
                    error_message = f"API Error {data['code']}: {data.get('code_message', 'No additional information provided.')}"
                    raise requests.HTTPError(error_message)
                # elapsed_time = time.time() - start_time
                #
                # minutes, seconds = divmod(elapsed_time, 60)
                # dados={'nome': name, 'nTitulo': data['data'][0]['titulo_eleitoral'], 'zona': data['data'][0]['uf'] + ' ' + data['data'][0]['zona']}
                # print(f'Dados da api: {dados} ')
                return {'nome': name, 'nTitulo': data['data'][0]['titulo_eleitoral'], 'zona': data['data'][0]['uf'] + ' ' + data['data'][0]['zona']}
            except requests.HTTPError as e:
                print(f"Erro na API: {e}. Tentativa {attempt + 1}/{max_attempts}.")
                # if attempt >= 1:
                self.timeout *= backoff_factor
                if attempt + 1 == max_attempts:
                    raise Exception("Máximo de tentativas atingidas.")
            except requests.RequestException as e:
                print(f"Erro na requisição: {e}. Tentativa {attempt + 1}/{max_attempts}.")
                if attempt + 1 == max_attempts:
                    raise Exception("Falha crítica de rede ou requisição.")

#
# # Uso da classe
# consulta = ConsultaTituloEleitoral(
#     token="VDRfLIYiiFqEy39v9fr6Q6c-1x4qyUTxzyhVdiIk"
# )
#
# query = {'birthdate' : "1997-07-02",
# 'mother' : "cleonice maria de castro",
# 'name' : "geraldo pereira de castro junior"}
#
#
# details = consulta.execute(
#     query['birthdate'], query['mother'], query['name']
# )
#
#
# if details is not None:
#     print("Detalhes extraídos:", details)
# else:
#     print("Falha ao extrair detalhes ou consulta não bem-sucedida.")
