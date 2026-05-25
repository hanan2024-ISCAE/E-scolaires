from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Etudiant


class RegisterEtudiantSerializer(serializers.ModelSerializer):

    matricule = serializers.CharField()
    filiere = serializers.CharField()
    niveau = serializers.CharField()
    photo = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'matricule',
            'filiere',
            'niveau',
            'photo'
        ]

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email déjà utilisé")

        return value

    def create(self, validated_data):

        matricule = validated_data.pop('matricule')
        filiere = validated_data.pop('filiere')
        niveau = validated_data.pop('niveau')
        photo = validated_data.pop('photo', None)

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            role='etudiant'
        )

        Etudiant.objects.create(
            user=user,
            matricule=matricule,
            filiere=filiere,
            niveau=niveau,
            photo=photo
        )

        return user