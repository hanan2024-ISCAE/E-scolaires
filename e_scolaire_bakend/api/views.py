import mimetypes
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import DemandeInscription, Note, Reclamation, RessourcePedagogique
from .permissions import IsAdmin, IsStudent
from .serializers import (
    DemandeInscriptionCreateSerializer,
    DemandeInscriptionSerializer,
    NoteSerializer,
    ReclamationCreateSerializer,
    ReclamationSerializer,
    RegisterEtudiantSerializer,
    RessourceCreateSerializer,
    RessourceSerializer,
    UserSerializer,
)

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_etudiant(request):

    serializer = RegisterEtudiantSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Inscription réussie"
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            "success": False,
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class DemandeInscriptionViewSet(ModelViewSet):
    queryset = DemandeInscription.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    http_method_names = ["get", "post", "head", "options"]

    def get_permissions(self):
        return [AllowAny()] if self.action == "create" else [IsAdmin()]

    def get_serializer_class(self):
        return DemandeInscriptionCreateSerializer if self.action == "create" else DemandeInscriptionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if s := self.request.query_params.get("statut"):
            qs = qs.filter(statut=s)
        return qs

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.save(password=make_password(ser.validated_data["password"]))
        return Response(DemandeInscriptionSerializer(d, context={"request": request}).data, status=201)

    @action(detail=True, methods=["post"])
    def valider(self, request, pk=None):
        d = self.get_object()
        if d.statut != "en_attente":
            return Response({"detail": "Déjà traitée."}, status=400)
        if User.objects.filter(username=d.matricule).exists():
            return Response({"detail": "Compte existant."}, status=400)
        u = User.objects.create(
            username=d.matricule, email=d.email, password=d.password,
            first_name=d.prenom, last_name=d.nom, matricule=d.matricule,
            filiere=d.filiere, niveau=d.niveau, role="student",
        )
        if d.photo:
            u.photo = d.photo
            u.save(update_fields=["photo"])
        d.statut, d.traite_par = "validee", request.user
        d.save(update_fields=["statut", "traite_par"])
        return Response({"demande": DemandeInscriptionSerializer(d, context={"request": request}).data})

    @action(detail=True, methods=["post"])
    def refuser(self, request, pk=None):
        d = self.get_object()
        if d.statut != "en_attente":
            return Response({"detail": "Déjà traitée."}, status=400)
        d.statut = "refusee"
        d.motif_refus = request.data.get("motif_refus", "")
        d.traite_par = request.user
        d.save(update_fields=["statut", "motif_refus", "traite_par"])
        return Response({"demande": DemandeInscriptionSerializer(d, context={"request": request}).data})


class MesNotesListView(ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Note.objects.filter(etudiant=self.request.user)


class ReclamationViewSet(ModelViewSet):
    http_method_names = ["get", "post", "head", "options"]

    def get_permissions(self):
        if self.action in ("create", "mes"):
            return [IsStudent()]
        return [IsAdmin()]

    def get_serializer_class(self):
        return ReclamationCreateSerializer if self.action == "create" else ReclamationSerializer

    def get_queryset(self):
        qs = Reclamation.objects.select_related("etudiant", "note")
        if s := self.request.query_params.get("statut"):
            qs = qs.filter(statut=s)
        return qs

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        r = ser.save(etudiant=request.user)
        return Response(ReclamationSerializer(r).data, status=201)

    @action(detail=False, methods=["get"])
    def mes(self, request):
        return Response(ReclamationSerializer(self.get_queryset().filter(etudiant=request.user), many=True).data)

    @action(detail=True, methods=["post"])
    def accepter(self, request, pk=None):
        r = self.get_object()
        if r.statut != "en_attente":
            return Response({"detail": "Déjà traitée."}, status=400)
        v = request.data.get("nouvelle_valeur")
        nouvelle = Decimal(str(v)) if v is not None else min(r.note.valeur + 1, 20)
        r.note.valeur = nouvelle
        r.note.save(update_fields=["valeur"])
        r.statut, r.nouvelle_valeur = "acceptee", nouvelle
        r.commentaire_admin = request.data.get("commentaire_admin", "")
        r.traite_par = request.user
        r.save()
        return Response(ReclamationSerializer(r).data)

    @action(detail=True, methods=["post"])
    def refuser(self, request, pk=None):
        r = self.get_object()
        if r.statut != "en_attente":
            return Response({"detail": "Déjà traitée."}, status=400)
        r.statut = "refusee"
        r.commentaire_admin = request.data.get("commentaire_admin", "")
        r.traite_par = request.user
        r.save()
        return Response(ReclamationSerializer(r).data)


class RessourceViewSet(ModelViewSet):
    queryset = RessourcePedagogique.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "head", "options"]

    def get_permissions(self):
        return [IsAdmin()] if self.action == "create" else [IsStudent()]

    def get_serializer_class(self):
        return RessourceCreateSerializer if self.action == "create" else RessourceSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        for p, f in [("type", "type_ressource"), ("module", "module__icontains"), ("niveau", "niveau"), ("search", "titre__icontains")]:
            if v := self.request.query_params.get(p):
                qs = qs.filter(**{f: v})
        return qs

    def list(self, request, *args, **kwargs):
        return Response(RessourceSerializer(self.get_queryset(), many=True).data)

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        o = ser.save(publie_par=request.user)
        return Response(RessourceSerializer(o).data, status=201)

    @action(detail=True, methods=["get"])
    def telecharger(self, request, pk=None):
        r = self.get_object()
        if not r.fichier:
            return Response({"detail": "Fichier introuvable."}, status=404)
        ct, _ = mimetypes.guess_type(r.fichier.name)
        return FileResponse(
            r.fichier.open("rb"),
            content_type=ct or "application/octet-stream",
            as_attachment=True,
            filename=r.fichier.name.split("/")[-1],
        )
