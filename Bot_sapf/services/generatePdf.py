import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import *
from django.conf import settings
import os


def fill_form(source_pdf, dados, output_path):
    print(f'local saida dentro da func{output_path}')
    # Mapeamento dos campos do formulário para os dados fornecidos
    campos_mapa = {
        'nome': dados['nome'],
        'data_d': dados['data_d'],
        'data_m': dados['data_m'],
        'data_a': dados['data_a'],
        'titulo_cidadao': dados['titulo'],
        'zona': dados['zona'],
        'nome_coletor': dados['nome_coletor'],
        'titulo_coletor': dados['titulo_coletor'] 
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
