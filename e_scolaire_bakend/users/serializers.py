from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DemandeInscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "matricule", "filiere", "niveau"]


class DemandeInscriptionSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = DemandeInscription
        fields = [
            "id", "prenom", "nom", "etudiant_nom", "email", "matricule", "filiere", "niveau",
            "photo_url", "statut", "motif_refus", "created_at",
        ]

    def get_etudiant_nom(self, obj):
        return f"{obj.prenom} {obj.nom}"

    def get_photo_url(self, obj):
        if obj.photo and (r := self.context.get("request")):
            return r.build_absolute_uri(obj.photo.url)
        return None


class DemandeInscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeInscription
        fields = ["prenom", "nom", "email", "password", "matricule", "filiere", "niveau", "photo"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, v):
        if DemandeInscription.objects.filter(email=v).exists() or User.objects.filter(email=v).exists():
            raise serializers.ValidationError("Email déjà utilisé.")
        return v

    def validate_matricule(self, v):
        if DemandeInscription.objects.filter(matricule=v, statut="en_attente").exists() or User.objects.filter(matricule=v).exists():
            raise serializers.ValidationError("Matricule déjà utilisé.")
        return v
