from rest_framework import serializers

from .models import Reclamation


class ReclamationSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    module = serializers.CharField(source="note.module", read_only=True)
    valeur_contestee = serializers.DecimalField(source="note.valeur", max_digits=4, decimal_places=2, read_only=True)

    class Meta:
        model = Reclamation
        fields = [
            "id", "etudiant", "etudiant_nom", "note", "module", "valeur_contestee",
            "motif", "statut", "commentaire_admin", "nouvelle_valeur", "created_at",
        ]

    def get_etudiant_nom(self, obj):
        return f"{obj.etudiant.first_name} {obj.etudiant.last_name}".strip() or obj.etudiant.username


class ReclamationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reclamation
        fields = ["note", "motif"]

    def validate_note(self, note):
        user = self.context["request"].user
        if note.etudiant_id != user.id:
            raise serializers.ValidationError("Note invalide.")
        if Reclamation.objects.filter(note=note, etudiant=user, statut="en_attente").exists():
            raise serializers.ValidationError("Réclamation déjà en attente.")
        return note
