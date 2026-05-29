from django.db import connection
from rest_framework import serializers

from users.models import User

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    etudiant_matricule = serializers.CharField(source="etudiant.matricule", read_only=True)
    publie_par_nom = serializers.CharField(source="publie_par.username", read_only=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "etudiant",
            "etudiant_nom",
            "etudiant_matricule",
            "module",
            "type_note",
            "valeur",
            "coefficient",
            "date_publication",
            "publie_par_nom",
        ]
        read_only_fields = ["id", "date_publication", "publie_par_nom"]

    def get_etudiant_nom(self, obj):
        full_name = obj.etudiant.get_full_name()
        return full_name or obj.etudiant.username


class PublierNoteSerializer(serializers.ModelSerializer):
    etudiant = serializers.CharField(write_only=True)
    module_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Note
        fields = ["id", "etudiant", "module_id", "module", "type_note", "valeur", "coefficient", "date_publication"]
        read_only_fields = ["id", "module", "coefficient", "date_publication"]

    def validate_etudiant(self, value):
        try:
            return User.objects.get(matricule=value, role="student")
        except User.DoesNotExist:
            try:
                return User.objects.get(username=value, role="student")
            except User.DoesNotExist as exc:
                raise serializers.ValidationError("Etudiant introuvable avec ce matricule ou username.") from exc

    def validate_valeur(self, value):
        if value < 0 or value > 20:
            raise serializers.ValidationError("La note doit etre entre 0 et 20.")
        return value

    def validate_module_id(self, value):
        with connection.cursor() as cursor:
            cursor.execute("SELECT intitule, coefficient FROM api_module WHERE id = %s", [value])
            row = cursor.fetchone()
        if not row:
            raise serializers.ValidationError("Module introuvable.")
        return {"intitule": row[0], "coefficient": int(row[1])}

    def create(self, validated_data):
        module = validated_data.pop("module_id")
        validated_data["module"] = module["intitule"]
        validated_data["coefficient"] = module["coefficient"]
        validated_data["publie_par"] = self.context["request"].user
        return super().create(validated_data)
