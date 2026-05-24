from django.conf import settings
from django.db import models


class Note(models.Model):
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes")
    module = models.CharField(max_length=150)
    type_note = models.CharField(max_length=20, default="examen")
    valeur = models.DecimalField(max_digits=4, decimal_places=2)
    coefficient = models.PositiveSmallIntegerField(default=4)
    date_publication = models.DateField(auto_now_add=True)
    publie_par = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")

    class Meta:
        ordering = ["-date_publication"]
