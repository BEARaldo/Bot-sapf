import requests
from bs4 import BeautifulSoup

def capturar_dados(html_response):
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

def api_consulta(cpf):
    # Configuração inicial, URL e cookies
    cookie_manual = {
        'wordpress_logged_in_dd8782f26a34dfd3c646a09580a7757b': 'thihft%40gmail.com%7C1713780026%7Cndq1j1f1cltUZQcJsBU295xW2G3MOxUO1U0Eolk9FWu%7C139d26a84406f74f1e4c4e3ea50efe95880c829c8f9f427a681bb636784ccd8a'
    }
    url = "https://deskdata.com.br/pessoas/"
    payload_cpf = {
        "key-select": "cpf",
        "cpf": cpf,
        "key-extra-select": "",
        "basic_data": "basic_data",
        "search_type": "people",
        "submit": "Consultar",
        "duplicate-query-confirm": "false"
    }
    # Faz a requisição POST
    response_post = requests.post(url, data=payload_cpf, cookies=cookie_manual, allow_redirects=False)

    # Verifica se houve redirecionamento
    if response_post.status_code == 302:
        redirect_url = response_post.headers['Location']
        response_get = requests.get(redirect_url, cookies=cookie_manual)
        # Usa a função capturar_dados para extrair as informações do HTML
        dados = capturar_dados(response_get.text)
        print(dados)  # Imprime os dados extraídos
    else:
        print("Solicitação falhou. Código de status:", response_post.status_code)

cpf = ''#insira o CPF
api_consulta(cpf)