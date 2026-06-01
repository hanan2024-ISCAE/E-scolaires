from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False})
    matiere = models.CharField(max_length=100)
    valeur = models.FloatField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name_plural = "Notes"

    def __str__(self):
        return f"{self.etudiant.username} - {self.matiere}: {self.valeur}"

class Reclamation(models.Model):
    STATUS_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('TRAITE', 'Traité'),
        ('REJETE', 'Rejeté'),
    ]
    
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='reclamations')
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE)
    motif = models.TextField(help_text="Expliquez pourquoi vous contestez cette note.")
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EN_ATTENTE')
    reponse = models.TextField(blank=True, null=True, help_text="Réponse de l'enseignant")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_creation']
        unique_together = ['note', 'etudiant']

    def __str__(self):
        return f"Réclamation de {self.etudiant.username} ({self.note.matiere}) - {self.statut}"