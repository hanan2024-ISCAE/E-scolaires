from django.conf import settings
from django.db import models


class RessourcePedagogique(models.Model):
    titre = models.CharField(max_length=255)
    type_ressource = models.CharField(max_length=20, default="cours")
    module = models.CharField(max_length=150)
    niveau = models.CharField(max_length=10, default="L3")
    annee_scolaire = models.CharField(max_length=9, default="2024-2025")
    fichier = models.FileField(upload_to="ressources/")
    publie_par = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
