import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image
from django.conf import settings
from pathlib import Path

from .models import PDFFile


class PDFManager:
    def __init__(self, name: str, author):
        self.name = name
        self.file_name = name if name.endswith('.pdf') else name + '.pdf'
        self.filepath = self.get_filepath
        self.author = author

    def save_file(self, pdf_buffer):
        """save file to filesystem and put a record into DB"""
        with open(self.filepath, 'wb') as pdf_file:
            pdf_file.write(pdf_buffer.getvalue())

        instance = PDFFile(name=self.file_name, author=self.author)
        instance.file_field.name = str(self.filepath)
        instance.save()

    @staticmethod
    def convert(image_files):
        """Create pdf file from images"""

        pdf_buffer = io.BytesIO()
        pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=letter)

        for image_file in image_files:
            # Open the image using Pillow
            image = Image.open(image_file)
            read_image = ImageReader(image)

            page_width = 21.0
            page_height = 29.7

            image_width, image_height = image.size
            aspect_ratio = image_height / image_width

            pdf_image_width = 20.5
            pdf_image_height = pdf_image_width * aspect_ratio

            width_ratio = image_width / page_width
            height_ratio = image_height / page_height

            if width_ratio > 1 or height_ratio > 1:
                max_ratio = max(width_ratio, height_ratio)
                image_width /= max_ratio
                image_height /= max_ratio

            # Draw the image on the PDF page
            pdf_canvas.drawImage(read_image, x=0.5*cm, y=28*cm - image_height*cm,
                                 width=pdf_image_width*cm,
                                 height=pdf_image_height*cm)

            # Add a new page to the PDF file for the next image
            pdf_canvas.showPage()

        # Save the PDF file
        pdf_canvas.save()
        pdf_buffer.seek(0)
        return pdf_buffer

    @property
    def get_filepath(self) -> Path:
        """calculates filename for pdf file"""

        # name the file
        abs_path_to_pdf = settings.MEDIA_ROOT / Path('pdfs') / self.file_name

        # if file with this name exists add suffix - number
        suffix = 1
        pdf_directory = settings.MEDIA_ROOT / 'pdfs'
        while abs_path_to_pdf.exists():
            file_name = f'{self.name}({str(suffix)}).pdf'
            suffix += 1
            abs_path_to_pdf = pdf_directory / file_name

        # Ensure directory exists
        pdf_directory.mkdir(parents=True, exist_ok=True)

        return abs_path_to_pdf
