from django.contrib import admin
from .models import Note, Reclamation

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'matiere', 'valeur', 'date_creation']
    list_filter = ['matiere', 'date_creation']
    search_fields = ['etudiant__username', 'matiere']
    readonly_fields = ['date_creation']

@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'note', 'statut', 'date_creation']
    list_filter = ['statut', 'date_creation']
    search_fields = ['etudiant__username', 'note__matiere']
    readonly_fields = ['date_creation', 'date_modification']
    fieldsets = (
        ('Informations', {
            'fields': ('note', 'etudiant', 'motif')
        }),
        ('Traitement', {
            'fields': ('statut', 'reponse')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
