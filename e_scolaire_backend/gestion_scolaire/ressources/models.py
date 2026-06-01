from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.conf import settings
import os

class RessourcePedagogique(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fichier = models.FileField(
        upload_to='ressources_pedagogiques/',
        validators=[FileExtensionValidator(allowed_extensions=settings.ALLOWED_RESOURCE_EXTENSIONS)]
    )
    enseignant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    date_publication = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_publication']
        verbose_name_plural = "Ressources Pédagogiques"

    def __str__(self):
        return self.titre

    def get_file_extension(self):
        """Retourne l'extension du fichier"""
        return os.path.splitext(self.fichier.name)[1][1:].lower()

    def get_file_size_mb(self):
        """Retourne la taille du fichier en MB"""
        return round(self.fichier.size / (1024 * 1024), 2)