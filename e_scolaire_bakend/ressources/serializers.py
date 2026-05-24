from rest_framework import serializers

from .models import RessourcePedagogique


class RessourceSerializer(serializers.ModelSerializer):
    taille = serializers.SerializerMethodField()

    class Meta:
        model = RessourcePedagogique
        fields = ["id", "titre", "type_ressource", "module", "niveau", "annee_scolaire", "taille", "created_at"]

    def get_taille(self, obj):
        try:
            return obj.fichier.size
        except (ValueError, OSError):
            return 0


class RessourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RessourcePedagogique
        fields = ["titre", "type_ressource", "module", "niveau", "annee_scolaire", "fichier"]
