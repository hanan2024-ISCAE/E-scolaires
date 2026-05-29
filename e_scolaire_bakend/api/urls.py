from django.urls import path
from .views import (
    NotesListView,
    PublierNoteView,
    ModulesListView,
    MesNotesListView,
    DropdownOptionsView
)

app_name = 'api'

urlpatterns = [
    # Admin endpoints
    path('notes/', NotesListView.as_view(), name='notes-list'),
    path('notes/publier/', PublierNoteView.as_view(), name='publier-note'),
    path('modules/', ModulesListView.as_view(), name='modules-list'),
    
    # Get dropdown options
    path('notes/dropdown-options/', DropdownOptionsView.as_view(), name='dropdown-options'),
    
    # Student endpoints
    path('mes-notes/', MesNotesListView.as_view(), name='mes-notes'),
]