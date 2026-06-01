from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Note, Reclamation
from .serializers import NoteSerializer, ReclamationSerializer, ReclamationDetailSerializer

class NoteViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter les notes de l'étudiant authentifié"""
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Les étudiants ne voient que leurs notes
        if self.request.user.is_staff:
            return Note.objects.all()
        return Note.objects.filter(etudiant=self.request.user)

class ReclamationViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les réclamations sur les notes"""
    serializer_class = ReclamationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Les enseignants voient toutes les réclamations
            return Reclamation.objects.all()
        # Les étudiants ne voient que leurs réclamations
        return Reclamation.objects.filter(etudiant=user)

    def get_serializer_class(self):
        if self.request.user.is_staff and self.action == 'retrieve':
            return ReclamationDetailSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        """Créer une nouvelle réclamation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Vérifier que l'étudiant ne peut réclamer que pour sa propre note
        note_id = request.data.get('note_id')
        try:
            note = Note.objects.get(id=note_id, etudiant=request.user)
        except Note.DoesNotExist:
            return Response(
                {"error": "Note introuvable ou action non autorisée."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier qu'il n'existe pas déjà une réclamation pour cette note
        if Reclamation.objects.filter(note=note, etudiant=request.user).exists():
            return Response(
                {"error": "Une réclamation existe déjà pour cette note."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def traiter(self, request, pk=None):
        """Action pour que l'enseignant traite une réclamation"""
        if not request.user.is_staff:
            return Response(
                {"error": "Seuls les enseignants peuvent traiter les réclamations."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reclamation = self.get_object()
        new_statut = request.data.get('statut')
        reponse = request.data.get('reponse', '')

        if new_statut not in ['TRAITE', 'REJETE']:
            return Response(
                {"error": "Le statut doit être 'TRAITE' ou 'REJETE'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        reclamation.statut = new_statut
        reclamation.reponse = reponse
        reclamation.save()

        serializer = self.get_serializer(reclamation)
        return Response(serializer.data)