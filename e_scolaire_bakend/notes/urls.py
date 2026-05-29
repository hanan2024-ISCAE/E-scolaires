# from django.urls import path

# from .views import MesNotesListView, ModulesListView, NotesListView, PublierNoteView

# urlpatterns = [
#     path("", NotesListView.as_view()),
#     path("modules/", ModulesListView.as_view()),
#     path("publier/", PublierNoteView.as_view()),
#     path("mes/", MesNotesListView.as_view()),
# ]
from django.urls import path
from api.views import (
    dropdown_options,
    notes_list,
    publier_note,
    modules_list,
    mes_notes,
)

urlpatterns = [
    # Admin endpoints
    path('', notes_list, name='notes-list'),
    path('publier/', publier_note, name='publier-note'),
    path('modules/', modules_list, name='modules-list'),
    
    # Get dropdown options
    path('dropdown-options/', dropdown_options, name='dropdown-options'),
    
    # Student endpoints
    path('mes-notes/', mes_notes, name='mes-notes'),
]