from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import DemandeInscription
from .permissions import IsAdmin
from .serializers import DemandeInscriptionCreateSerializer, DemandeInscriptionSerializer, UserSerializer

User = get_user_model()


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class StudentsListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return User.objects.filter(role="student").order_by("last_name", "first_name", "username")


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
