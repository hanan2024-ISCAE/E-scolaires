from rest_framework.generics import CreateAPIView, ListAPIView

from users.permissions import IsAdmin, IsStudent

from .models import Note
from .serializers import NoteSerializer, PublierNoteSerializer


class NotesListView(ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAdmin]
    queryset = Note.objects.select_related("etudiant", "publie_par")


class PublierNoteView(CreateAPIView):
    serializer_class = PublierNoteSerializer
    permission_classes = [IsAdmin]


class MesNotesListView(ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Note.objects.filter(etudiant=self.request.user).select_related("etudiant", "publie_par")
