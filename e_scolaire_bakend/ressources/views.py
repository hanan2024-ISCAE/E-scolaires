import mimetypes

from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsAdmin, IsStudent

from .models import RessourcePedagogique
from .serializers import RessourceCreateSerializer, RessourceSerializer


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
