from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from api.models import DemandeInscription, Note, Reclamation, RessourcePedagogique

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin, _ = User.objects.update_or_create(
            username="admin",
            defaults=dict(
                email="admin@escolaire.ma", password=make_password("admin123"),
                first_name="Admin", last_name="System", role="admin", is_staff=True, is_superuser=True,
            ),
        )
        student, _ = User.objects.update_or_create(
            username="20230456",
            defaults=dict(
                email="ahmed@mail.com", password=make_password("student123"),
                first_name="Ahmed", last_name="Benali", role="student",
                matricule="20230456", filiere="Informatique", niveau="L3",
            ),
        )
        DemandeInscription.objects.update_or_create(
            matricule="20230499",
            defaults=dict(
                prenom="Fatima", nom="Zahra", email="fatima@mail.com",
                password=make_password("temp123"), filiere="Mathématiques", niveau="L1", statut="en_attente",
            ),
        )
        note, _ = Note.objects.update_or_create(
            etudiant=student, module="Analyse Numérique", type_note="tp",
            defaults=dict(valeur=Decimal("11"), coefficient=3, publie_par=admin),
        )
        Reclamation.objects.get_or_create(
            etudiant=student, note=note, statut="en_attente",
            defaults=dict(motif="Erreur de correction TP"),
        )
        res, _ = RessourcePedagogique.objects.get_or_create(
            titre="Cours — Algorithmes Avancés",
            defaults=dict(type_ressource="cours", module="Algorithmes & Structures", niveau="L3", publie_par=admin),
        )
        if not res.fichier:
            res.fichier.save("demo-algo.pdf", ContentFile(b"%PDF-1.4 demo"), save=True)
