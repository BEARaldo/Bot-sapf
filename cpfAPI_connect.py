import requests

# realize GET para obter os cookies - verificar necessidade
# response_get = requests.get('https://deskdata.com.br/entrar/')#configurar Json
# cookies = response_get.cookies

cookie_manual = {'wordpress_logged_in_dd8782f26a34dfd3c646a09580a7757b':'thihft%40gmail.com%7C1713780026%7Cndq1j1f1cltUZQcJsBU295xW2G3MOxUO1U0Eolk9FWu%7C139d26a84406f74f1e4c4e3ea50efe95880c829c8f9f427a681bb636784ccd8a'}#->json; Verificar se varia


deskdata_logon = { #JSON
    'log': 'thihft@gmail.com',
    'pwd': 'thiago123',
    'wp-submit': 'Entrar',
    'redirect_to': 'https://deskdata.com.br/wp-admin/',
    'testcookie': '1'
}
url = "https://deskdata.com.br/pessoas/" #json
def api_consulta(cpf):
    payload_cpf = {
        "key-select": "cpf",
        "cpf": cpf,
        "key-extra-select": "",
        "basic_data": "basic_data",
        "search_type": "people",
        "submit": "Consultar",
        "duplicate-query-confirm": "false"
    }
    response_post = requests.post(url, data=payload_cpf, cookies=cookie_manual)

    if response_post.status_code == 302:
        print("Redirecionamento encontrado.")
        print("Localização do redirecionamento:", response_post.headers['Location'])
        print(response_post.text)
    else:
        print("Solicitação falhou. Código de status:", response_post.status_code)
        print(response_post.text)
        # print(response_post.cookies)
        req_prof = requests.get('https://deskdata.com.br/wp-admin/profile.php', data=deskdata_logon, cookies=cookie_manual)
        print('req_prof')
        print(req_prof.text)
        print(req_prof.cookies)

def capturar_dados(response):
    #capturar os dados do response da pagina
'''
        Capturar nome, data nascimento, nome mae
		<h5>Dados básicos</h5>
									<div class="div-overflow-mobile">
							  	  <table class="table table-sm table-hover">
							    		<tr class="clickable" data-toggle="tooltip" data-placement="top" title="Clique para copiar">
							    			<th class="w-label">Nome</th>
							    			<td class="data"></td>
							    		</tr>
							  				<tr class="clickable" data-toggle="tooltip" data-placement="top" title="Clique para copiar">
							  					<th class="w-label">CPF</th>
							  					<td class="data"></td>
						  					</tr>
							  				<tr class="clickable" data-toggle="tooltip" data-placement="top" title="Clique para copiar">
							  					<th class="w-label">Situação do CPF</th>
							  					<td class="data"></td>
						  					</tr>
								      	<tr class="clickable" data-toggle="tooltip" data-placement="top" title="Clique para copiar"><th class="w-label">Gênero</th><td class="data">Masculino</td></tr>
								      	<tr class="clickable" data-toggle="tooltip" data-placement="top" title="Clique para copiar"><th class="w-label">Nascimento</th><td class="data"></td></tr>
								      	<tr class="clickable" data-toggle="tooltip" data-placement="top" title="Clique para copiar"><th class="w-label">Nacionalidade</th><td class="data">Brasileira</td></tr>
								      	<tr class="clickable" data-toggle="tooltip" data-placement="top" title="Clique para copiar"><th class="w-label">Idade</th><td class="data"></td></tr>
					      				<tr class="clickable" data-toggle="tooltip" data-placement="top" title="Clique para copiar"><th class="w-label">Nome do pai</th><td class="data">/td></tr>

								      	<tr class="clickable" data-toggle="tooltip" data-placement="top" title="Clique para copiar"><th class="w-label">Nome da mãe</th><td class="data">/td></tr>
								      	<tr class="clickable" data-toggle="tooltip" data-placement="top" title="Clique para copiar"><th class="w-label">Signo</th><td class="data">Cancer</td></tr>

					  					</table>
'''
        #return dict dos dados

api_consulta(cpf)