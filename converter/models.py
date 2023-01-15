import uuid
from pathlib import Path
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class PDFFile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    file_field = models.FileField(upload_to='pdfs', verbose_name='document')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def path(self):
        file_rel_path = 'pdfs\\' + str(self.name)
        BASE_DIR = Path(__file__).resolve().parent.parent
        return BASE_DIR / Path('media') / file_rel_path

    def delete(self, *args, **kwargs):
        if self.file_field:
            self.file_field.storage.delete(self.file_field.name)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=PDFFile)
def PDFFile_delete(sender, instance, **kwargs):
    instance.file_field.delete(False)
