from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField(max_length=20, default="student")
    matricule = models.CharField(max_length=20, blank=True)
    filiere = models.CharField(max_length=100, blank=True)
    niveau = models.CharField(max_length=10, blank=True)
    photo = models.ImageField(upload_to="users/photos/", blank=True, null=True)

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser


class DemandeInscription(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    matricule = models.CharField(max_length=20, unique=True)
    filiere = models.CharField(max_length=100)
    niveau = models.CharField(max_length=10)
    photo = models.ImageField(upload_to="inscriptions/photos/", blank=True, null=True)
    statut = models.CharField(max_length=20, default="en_attente")
    motif_refus = models.TextField(blank=True)
    traite_par = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
