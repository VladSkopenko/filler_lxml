from pdfrw import PdfReader


def list_pdf_form_fields(pdf_path: str):
    pdf = PdfReader(pdf_path)
    field_names = set()
    for page in pdf.pages:
        annotations = page.get('/Annots') or []
        for annotation in annotations:
            field_name = annotation.get('/T')
            if field_name:
                field_names.add(field_name.to_unicode().strip('()'))
    return field_names


# Использование:
fields = list_pdf_form_fields('inbulk_ttn.pdf')
for name in fields:
    print(name)
