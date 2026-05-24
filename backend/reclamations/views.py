from decimal import Decimal

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsAdmin, IsStudent

from .models import Reclamation
from .serializers import ReclamationCreateSerializer, ReclamationSerializer


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
