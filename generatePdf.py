import PyPDF2


def update_pdf_contents(data, input_pdf_path, output_pdf_path):
    # Open the existing PDF
    # data = list(data.values())
    # data_index = 0
    with open(input_pdf_path, "rb") as infile:
        reader = PyPDF2.PdfReader(infile)
        writer = PyPDF2.PdfWriter()

        # Iterate through each page in the PDF
        for page in reader.pages:
            # Check if there are annotations
            if "/Annots" in page:
                annotations = page["/Annots"]
                for annot in annotations:
                    obj = annot.get_object()
                    if obj["/Subtype"] == "/FreeText":
                        field_name = obj.get("/NM", "")
                        if field_name in data:
                            print(obj)
                            if "/AP" in obj:
                                del obj["/AP"]
                            obj.update({
                                PyPDF2.generic.NameObject("/Contents"): PyPDF2.generic.TextStringObject(data[field_name]),
                                # PyPDF2.generic.NameObject("/CA"): PyPDF2.generic.FloatObject(1)
                            })
                            print(obj)

                            print(f"New content: {obj['/Contents']}")
            # Add the updated page to the writer
            writer.add_page(page)

        # Write out the updated PDF
        with open(output_pdf_path, "wb") as outfile:
            writer.write(outfile)

base_pdf_path = './ficha_apoio.pdf'
dados = {'nome': 'Geraldo Pereira', 'data1': '22', 'data2':'33','data3':'4444', 'titulo': '025239362089', 'zona': 'DF 005'}
# dados = ['data1', 'nome', 'data2', 'data3', 'titulo', 'zona', 'nomeColetor', 'tituloColetor']
update_pdf_contents(dados, base_pdf_path, "./updated.pdf")