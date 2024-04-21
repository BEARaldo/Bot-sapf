import requests

class ConsultaTituloEleitoral:
    def __init__(self, token):
        self.url = 'https://api.infosimples.com/api/v2/consultas/tse/titulo'
        self.token = token
        self.timeout = 100
        self.response_json = None

    def execute(self, birthdate, mother, name):
        payload = {
            "birthdate": birthdate,
            "mother": mother,
            "name": name,
            "token": self.token,
            "timeout": self.timeout
        }
        response = requests.post(self.url, payload)
        self.response_json = response.json()
        response.close()

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




# Uso da classe
consulta = ConsultaTituloEleitoral(
    token="TfOKDyyD-wrvUmN9o5yPzRq3rDGg_UiY4sJ8GRGg"
)

query = {'birthdate' : "1997-07-02",
'mother' : "cleonice maria de castro",
'name' : "geraldo pereira de castro junior"}

consulta.execute(
    query['birthdate'], query['mother'], query['name']
)

details = consulta.extract_details()

if details is not None:
    print("Detalhes extraídos:", details)
else:
    print("Falha ao extrair detalhes ou consulta não bem-sucedida.")