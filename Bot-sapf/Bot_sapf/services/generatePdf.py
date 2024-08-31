import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import *
from django.conf import settings
import os


def fill_form(source_pdf, dados, output_path):
    print(output_path)
    # Mapeamento dos campos do formulário para os dados fornecidos
    campos_mapa = {
        'nome': dados['nome'],
        'data_d': dados['data_d'],
        'data_m': dados['data_m'],
        'data_a': dados['data_a'],
        'titulo_cidadao': dados['titulo'],
        'zona': dados['zona'],
        'nome_coletor': 'Coletor Padrão',  # Exemplo de valor padrão, caso necessário
        'titulo_coletor': '12345678'  # Exemplo de valor padrão, caso necessário
    }

    # Carrega o PDF original
    leitor_pdf = PdfReader(source_pdf)
    escritor_pdf = PdfWriter()

    # Copia as páginas do PDF original e preenche os campos do formulário
    for pagina in leitor_pdf.pages:
        # Atualiza os campos do formulário com os dados
        if '/Annots' in pagina:
            for annot in pagina['/Annots']:
                campo_form = annot.get_object().get('/T')
                if campo_form in campos_mapa:
                    # print(annot.get_object())
                    annot.get_object().update({
                        NameObject('/V'): TextStringObject(campos_mapa[campo_form])
                    })
                    print('atualizado')

        # Adiciona a página modificada ao novo documento PDF
        escritor_pdf.add_page(pagina)

    # Salva o novo PDF preenchido
    with open(output_path, 'wb') as novo_pdf:
        try:
            escritor_pdf.write(novo_pdf)
            print('salvo')
        except Exception as e:
            print(f'erro:{e}')
    return output_path
# base_pdf_path = './ficha_apoio.pdf'
# dados = {'nome': 'Geraldo Pereira', 'data1': '22', 'data2':'33','data3':'4444', 'titulo': '025239362089', 'zona': 'DF 005'}
# # # dados = ['data1', 'nome', 'data2', 'data3', 'titulo', 'zona', 'nomeColetor', 'tituloColetor']
# update_pdf_contents(dados, base_pdf_path, "./updated.pdf")