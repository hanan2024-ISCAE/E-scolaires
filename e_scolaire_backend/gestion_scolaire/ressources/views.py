from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from .models import RessourcePedagogique
from .serializers import RessourcePedagogiqueSerializer

class RessourcePedagogiqueViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les ressources pédagogiques"""
    serializer_class = RessourcePedagogiqueSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Tous les utilisateurs authentifiés peuvent voir les ressources
        return RessourcePedagogique.objects.all().order_by('-date_publication')

    def create(self, request, *args, **kwargs):
        """Créer une nouvelle ressource pédagogique"""
        # Seuls les enseignants (staff) peuvent créer
        if not request.user.is_staff:
            return Response(
                {"error": "Accès refusé. Seuls les enseignants peuvent publier."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """L'enseignant est automatiquement défini"""
        serializer.save(enseignant=self.request.user)

    def update(self, request, *args, **kwargs):
        """Mettre à jour une ressource (seul le créateur peut la modifier)"""
        resource = self.get_object()
        if request.user != resource.enseignant and not request.user.is_superuser:
            return Response(
                {"error": "Vous n'avez pas le droit de modifier cette ressource."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Supprimer une ressource (seul le créateur peut la supprimer)"""
        resource = self.get_object()
        if request.user != resource.enseignant and not request.user.is_superuser:
            return Response(
                {"error": "Vous n'avez pas le droit de supprimer cette ressource."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def mes_ressources(self, request):
        """Récupérer les ressources publiées par l'enseignant authentifié"""
        if not request.user.is_staff:
            return Response(
                {"error": "Seuls les enseignants ont des ressources."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        ressources = RessourcePedagogique.objects.filter(enseignant=request.user)
        serializer = self.get_serializer(ressources, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def telecharger(self, request, pk=None):
        """Générer un lien de téléchargement pour la ressource"""
        resource = self.get_object()
        return Response({
            "titre": resource.titre,
            "url_telechargement": resource.fichier.url,
            "taille_mb": resource.get_file_size_mb(),
            "extension": resource.get_file_extension()
        })