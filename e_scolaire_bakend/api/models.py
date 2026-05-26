from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField(max_length=20, default="student")
    matricule = models.CharField(max_length=20, blank=True)
    filiere = models.CharField(max_length=100, blank=True)
    niveau = models.CharField(max_length=10, blank=True)
    photo = models.ImageField(upload_to="photos_etudiants/", blank=True, null=True)

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
    photo = models.ImageField(upload_to="photos_etudiants/", blank=True, null=True)
    statut = models.CharField(max_length=20, default="en_attente")
    motif_refus = models.TextField(blank=True)
    traite_par = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Note(models.Model):
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    module = models.CharField(max_length=150)
    type_note = models.CharField(max_length=20, default="examen")
    valeur = models.DecimalField(max_digits=4, decimal_places=2)
    coefficient = models.PositiveSmallIntegerField(default=4)
    date_publication = models.DateField(auto_now_add=True)
    publie_par = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="+")

    class Meta:
        ordering = ["-date_publication"]


class Reclamation(models.Model):
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reclamations")
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="reclamations")
    motif = models.TextField()
    statut = models.CharField(max_length=20, default="en_attente")
    commentaire_admin = models.TextField(blank=True)
    nouvelle_valeur = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    traite_par = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class RessourcePedagogique(models.Model):
    titre = models.CharField(max_length=255)
    type_ressource = models.CharField(max_length=20, default="cours")
    module = models.CharField(max_length=150)
    niveau = models.CharField(max_length=10, default="L3")
    annee_scolaire = models.CharField(max_length=9, default="2024-2025")
    fichier = models.FileField(upload_to="ressources/")
    publie_par = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
