import requests

# Realize o método GET para obter os cookies
response_get = requests.get('https://deskdata.com.br/entrar/')
cookies = response_get.cookies

cookie_manual = {'wordpress_logged_in_dd8782f26a34dfd3c646a09580a7757b':'thihft%40gmail.com%7C1713780026%7Cndq1j1f1cltUZQcJsBU295xW2G3MOxUO1U0Eolk9FWu%7C139d26a84406f74f1e4c4e3ea50efe95880c829c8f9f427a681bb636784ccd8a'}

url = "https://deskdata.com.br/pessoas/"
payload_cpf = {
    "key-select": "cpf",
    "cpf": "39836062882",
    "key-extra-select": "",
    "basic_data": "basic_data",
    "search_type": "people",
    "submit": "Consultar",
    "duplicate-query-confirm": "false"
}

# Utilize os cookies obtidos para realizar o método POST
payload = {
    'log': 'thihft@gmail.com',
    'pwd': 'thiago123',
    'wp-submit': 'Entrar',
    'redirect_to': 'https://deskdata.com.br/wp-admin/',
    'testcookie': '1'
}

response_post = requests.post('https://deskdata.com.br/pessoas/', data=payload_cpf, cookies=cookie_manual)

# Verifique o status da resposta e imprima o resultado
if response_post.status_code == 302:
    print("Redirecionamento encontrado.")
    print("Localização do redirecionamento:", response_post.headers['Location'])
    print(response_post.text)
else:
    print("Solicitação falhou. Código de status:", response_post.status_code)
    print(response_post.text)
    print(cookies)
    # print(response_post.cookies)
    req_prof = requests.get('https://deskdata.com.br/wp-admin/profile.php', data=payload, cookies=cookie_manual)
    print('req_prof')
    print(req_prof.text)
    print(req_prof.cookies)