
from django.db import models
from django.contrib.auth.models import AbstractUser

# =====================================================================
# 1. CLASSE USER (Héritage basé sur le modèle de base Django personnalisé)
# =====================================================================
class User(AbstractUser):
    # AbstractUser contient déjà : id, username, email, password
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('etudiant', 'Etudiant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)



# =====================================================================
# 2. CLASSE ADMIN (Hérite de User)
# =====================================================================
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='admin_profile')
    departement = models.CharField(max_length=100)


# =====================================================================
# 3. CLASSE ETUDIANT (Hérite de User) avec l'attribut PHOTO ajouté
# =====================================================================
class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='etudiant_profile')
    matricule = models.CharField(max_length=50, unique=True)
    filiere = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos_etudiants/', null=True, blank=True)

    


# =====================================================================
# 4. CLASSE LOGEMENT
# =====================================================================
class Logement(models.Model):
    capacite = models.IntegerField()
    numero = models.CharField(max_length=20)
    statut = models.CharField(max_length=50)
    
    # Relation "demande" entre Etudiant et Logement
    etudiants = models.ManyToManyField(Etudiant, related_name='logements_demandes', blank=True)



# =====================================================================
# 5. CLASSE MODULE
# =====================================================================
class Module(models.Model):
    intitule = models.CharField(max_length=100)
    coefficient = models.FloatField()
    semestre = models.CharField(max_length=50)

    


# =====================================================================
# 6. CLASSE NOTE
# =====================================================================
class Note(models.Model):
    type = models.CharField(max_length=50)  # Ex: DS, Examen
    valeur = models.FloatField()
    matiere = models.CharField(max_length=100)
    datePublication = models.DateField()
    
    # Relations d'après le diagramme
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name='notes_publiees')
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='notes_associees')

    


# =====================================================================
# 7. CLASSE RECLAMATION
# =====================================================================
class Reclamation(models.Model):
    objet = models.CharField(max_length=150)
    motif = models.TextField()
    statut = models.CharField(max_length=50, default='En attente')
    dateCreation = models.DateField(auto_now_add=True)
    
    # Relations
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='reclamations_soumises')
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name='reclamations_traitees')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='reclamations_concernees')

    


# =====================================================================
# 8. CLASSE RESSOURCE
# =====================================================================
class Ressource(models.Model):
    type = models.CharField(max_length=50)
    module_nom = models.CharField(max_length=100) # string module dans l'UML
    niveau = models.CharField(max_length=50)
    annee = models.CharField(max_length=10)
    fichier = models.FileField(upload_to='ressources/')
    
    # Relations
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, related_name='ressources_publiees')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='ressources_possedees')

    