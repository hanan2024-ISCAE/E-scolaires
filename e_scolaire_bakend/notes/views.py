from rest_framework.generics import ListAPIView

from users.permissions import IsStudent

from .models import Note
from .serializers import NoteSerializer


class MesNotesListView(ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Note.objects.filter(etudiant=self.request.user)
