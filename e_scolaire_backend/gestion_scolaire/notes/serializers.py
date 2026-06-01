from rest_framework import serializers
from .models import Note, Reclamation
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']

class NoteSerializer(serializers.ModelSerializer):
    etudiant = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'etudiant', 'matiere', 'valeur', 'date_creation']
        read_only_fields = ['id', 'date_creation']

class ReclamationSerializer(serializers.ModelSerializer):
    etudiant = UserSerializer(read_only=True)
    note = NoteSerializer(read_only=True)
    note_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Reclamation
        fields = ['id', 'note', 'note_id', 'etudiant', 'motif', 'statut', 'reponse', 'date_creation', 'date_modification']
        read_only_fields = ['id', 'etudiant', 'statut', 'reponse', 'date_creation', 'date_modification']

    def create(self, validated_data):
        # L'étudiant est automatiquement défini à partir de la requête
        validated_data['etudiant'] = self.context['request'].user
        return super().create(validated_data)

class ReclamationDetailSerializer(serializers.ModelSerializer):
    """Serializer pour les enseignants qui modifient le statut et ajoutent une réponse"""
    etudiant = UserSerializer(read_only=True)
    note = NoteSerializer(read_only=True)

    class Meta:
        model = Reclamation
        fields = ['id', 'note', 'etudiant', 'motif', 'statut', 'reponse', 'date_creation', 'date_modification']
        read_only_fields = ['id', 'note', 'etudiant', 'motif', 'date_creation']
