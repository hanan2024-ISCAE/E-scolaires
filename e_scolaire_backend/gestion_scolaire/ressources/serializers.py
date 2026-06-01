from rest_framework import serializers
from .models import RessourcePedagogique
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']

class RessourcePedagogiqueSerializer(serializers.ModelSerializer):
    enseignant = UserSerializer(read_only=True)
    file_extension = serializers.SerializerMethodField()
    file_size_mb = serializers.SerializerMethodField()

    class Meta:
        model = RessourcePedagogique
        fields = ['id', 'titre', 'description', 'fichier', 'enseignant', 'file_extension', 'file_size_mb', 'date_publication', 'date_modification']
        read_only_fields = ['id', 'enseignant', 'date_publication', 'date_modification']

    def get_file_extension(self, obj):
        return obj.get_file_extension()

    def get_file_size_mb(self, obj):
        return obj.get_file_size_mb()

    def validate_fichier(self, value):
        """Valide la taille du fichier"""
        from django.conf import settings
        if value.size > settings.MAX_RESOURCE_FILE_SIZE:
            raise serializers.ValidationError(
                f"La taille du fichier dépasse le maximum autorisé ({settings.MAX_RESOURCE_FILE_SIZE / (1024 * 1024)} MB)."
            )
        return value
