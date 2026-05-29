from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Etudiant, Admin


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

class EtudiantListSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        source='user.first_name'
    )

    last_name = serializers.CharField(
        source='user.last_name'
    )

    class Meta:
        model = Etudiant

        fields = [
            'matricule',
            'filiere',
            'niveau',
            'photo',
            'first_name',
            'last_name',
        ]


class EtudiantSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        source='user.username'
    )

    last_name = serializers.CharField(
        source='user.last_name'
    )

    email = serializers.CharField(
        source='user.email'
    )

    class Meta:

        model = Etudiant

        fields = [
            'first_name',
            'last_name',
            'email',
            'matricule',
            'filiere',
            'niveau',
            'photo'
        ]

class AdminSerializer(serializers.ModelSerializer):

    class Meta:

        model = Admin

        fields = '__all__'
    
class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField()

from .models import Attestation


class AttestationSerializer(serializers.ModelSerializer):

    fichier_url = serializers.SerializerMethodField()

    class Meta:

        model = Attestation

        fields = [
            "id",
            "type_attestation",
            "fichier",
            "fichier_url",
            "date_creation"
        ]

    def get_fichier_url(self, obj):

        request = self.context.get("request")

        if obj.fichier:

            return request.build_absolute_uri(
                obj.fichier.url
            )

        return None