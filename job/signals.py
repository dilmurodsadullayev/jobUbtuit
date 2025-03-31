from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import Document

@receiver(pre_delete, sender=Document)
def delete_files_on_delete(sender, instance, **kwargs):
    file_fields = [instance.passport, instance.objective, instance.diploma, instance.language_certificate, instance.benefits]

    for file_field in file_fields:
        if file_field and file_field.name:
            if default_storage.exists(file_field.name):
                default_storage.delete(file_field.name)
