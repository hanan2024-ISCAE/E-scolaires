from django.contrib import admin
from .models import RessourcePedagogique

@admin.register(RessourcePedagogique)
class RessourcePedagogiqueAdmin(admin.ModelAdmin):
    list_display = ['titre', 'enseignant', 'get_file_extension', 'get_file_size_mb', 'date_publication']
    list_filter = ['date_publication', 'enseignant']
    search_fields = ['titre', 'description', 'enseignant__username']
    readonly_fields = ['date_publication', 'date_modification', 'get_file_extension', 'get_file_size_mb']
    fieldsets = (
        ('Informations', {
            'fields': ('titre', 'description', 'enseignant')
        }),
        ('Fichier', {
            'fields': ('fichier', 'get_file_extension', 'get_file_size_mb')
        }),
        ('Dates', {
            'fields': ('date_publication', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
