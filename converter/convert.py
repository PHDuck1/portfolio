from PIL import Image
from django.conf import settings
from pathlib import Path

from .models import PDFFile


def make_pdf(files, name: str, author):
    # Collecting list of files
    image_list = [Image.open(file.temporary_file_path()) for file in files]

    # add .pdf suffix
    file_name = name if name.endswith('.pdf') else name + '.pdf'

    abs_path_to_pdf = settings.MEDIA_ROOT / Path('pdfs') / file_name

    suffix = 1
    while abs_path_to_pdf.exists():
        file_name = f'{name}({str(suffix)}).pdf'
        suffix += 1
        abs_path_to_pdf = settings.MEDIA_ROOT / Path('pdfs') / file_name

    image_list[0].save(abs_path_to_pdf, save_all=True, append_images=image_list[1:])

    print(abs_path_to_pdf)
    # if object not in model saving it
    instance = PDFFile(name=file_name, author=author)
    instance.file_field.name = str(abs_path_to_pdf)
    instance.save()
