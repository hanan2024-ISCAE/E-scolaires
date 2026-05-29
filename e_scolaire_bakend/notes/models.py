from django.conf import settings
from django.db import models


class Module(models.Model):
    intitule = models.CharField(max_length=100)
    coefficient = models.DecimalField(max_digits=4, decimal_places=2, default=1)
    semestre = models.CharField(max_length=50)
    
    class Meta:
        ordering = ['intitule']
    
    def __str__(self):
        return self.intitule


class Note(models.Model):
    TYPES = [
        ('examen', 'Examen'),
        ('tp', 'TP'),
        ('td', 'TD'),
        ('controle', 'Contrôle'),
    ]
    
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="notes")  # ✅ FIXED: ForeignKey instead of CharField
    type_note = models.CharField(max_length=20, choices=TYPES, default="examen")
    valeur = models.DecimalField(max_digits=4, decimal_places=2)
    coefficient = models.PositiveSmallIntegerField(default=1)
    date_publication = models.DateField(auto_now_add=True)
    publie_par = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="notes_publiees")

    class Meta:
        ordering = ["-date_publication"]
        unique_together = ['etudiant', 'module', 'type_note']  # Prevent duplicate notes

    def __str__(self):
        return f"{self.etudiant.username} - {self.module.intitule}: {self.valeur}/20"







# from django.conf import settings
# from django.db import models


# class Note(models.Model):
#     etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes")
#     module = models.CharField(max_length=150)
#     type_note = models.CharField(max_length=20, default="examen")
#     valeur = models.DecimalField(max_digits=4, decimal_places=2)
#     coefficient = models.PositiveSmallIntegerField(default=4)
#     date_publication = models.DateField(auto_now_add=True)
#     publie_par = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")

#     class Meta:
#         ordering = ["-date_publication"]
