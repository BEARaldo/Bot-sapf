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
def update_pdf_contents(data, input_pdf_path):
    # Open the existing PDF
    # data = list(data.values())
    # data_index = 0
    with open(input_pdf_path, "rb") as infile:
        reader = PyPDF2.PdfReader(infile)
        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            if "/Annots" in page:
                annotations = page["/Annots"]
                for annot in annotations:
                    obj = annot.get_object()
                    if obj["/Subtype"] == "/FreeText":
                        field_name = obj.get("/NM", "")
                        if field_name in data:
                            print(f"Antes:{obj}")
                            if "/AP" in obj:
                                ap = obj.get("/AP", "")
                                print(ap)
                                del obj["/AP"]
                            new_content = data[obj.get("/NM")]
                            obj.update({
                                PyPDF2.generic.NameObject("/Contents"): PyPDF2.generic.TextStringObject(data[field_name]),
                                # PyPDF2.generic.NameObject("/CA"): PyPDF2.generic.FloatObject(1)
                                # PyPDF2.generic.NameObject("/AP"): PyPDF2.generic.DictionaryObject(ap)
                            })

                            # Atualizar a appearance stream
                            rect = obj["/Rect"]
                            ap_stream = f"q 1 0 0 1 {rect[0]} {rect[1]} cm BT /Helv 11 Tf 0 0 0 rg ({new_content}) Tj ET Q"
                            stream_obj = PyPDF2.generic.DictionaryObject(ap)
                            # stream_obj._data = ap_stream.encode("utf-8")
                            obj.update({
                                "/AP": PyPDF2.generic.DictionaryObject({
                                    "/N": stream_obj
                                })
                            })

                            print(f"dpf:{obj}")

                            print(f"New content: {obj['/Contents']}")
            # Add the updated page to the writer
            writer.add_page(page)

        # Write out the updated PDF
        # pdf_file_path = os.path.join(settings.STATIC_ROOT, 'pdfs', 'gerado.pdf')

        output_pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'gerado.pdf')
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
        with open(output_pdf_path, "wb") as outfile:
            writer.write(outfile)
            print("salvo")
        return output_pdf_path
# base_pdf_path = './ficha_apoio.pdf'
# dados = {'nome': 'Geraldo Pereira', 'data1': '22', 'data2':'33','data3':'4444', 'titulo': '025239362089', 'zona': 'DF 005'}
# # # dados = ['data1', 'nome', 'data2', 'data3', 'titulo', 'zona', 'nomeColetor', 'tituloColetor']
# update_pdf_contents(dados, base_pdf_path, "./updated.pdf")