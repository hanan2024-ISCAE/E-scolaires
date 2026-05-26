from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import DemandeInscription, Note, Reclamation, RessourcePedagogique, User

UserModel = get_user_model()


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
            role='etudiant',
            matricule=matricule,
            filiere=filiere,
            niveau=niveau,
            photo=photo,
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
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
        if DemandeInscription.objects.filter(email=v).exists() or UserModel.objects.filter(email=v).exists():
            raise serializers.ValidationError("Email déjà utilisé.")
        return v

    def validate_matricule(self, v):
        if DemandeInscription.objects.filter(matricule=v, statut="en_attente").exists() or UserModel.objects.filter(matricule=v).exists():
            raise serializers.ValidationError("Matricule déjà utilisé.")
        return v


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "module", "type_note", "valeur", "coefficient", "date_publication"]


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
