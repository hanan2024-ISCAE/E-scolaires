from django.conf import settings
from django.db import models


class Reclamation(models.Model):
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reclamations")
    note = models.ForeignKey("notes.Note", on_delete=models.CASCADE, related_name="reclamations")
    motif = models.TextField()
    statut = models.CharField(max_length=20, default="en_attente")
    commentaire_admin = models.TextField(blank=True)
    nouvelle_valeur = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    traite_par = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
