from django.urls import path

from .views import MesNotesListView, NotesListView, PublierNoteView

urlpatterns = [
    path("", NotesListView.as_view()),
    path("publier/", PublierNoteView.as_view()),
    path("mes/", MesNotesListView.as_view()),
]
