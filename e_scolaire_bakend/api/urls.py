from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_etudiant, name='register'),
    path(
        'etudiants/',
        liste_etudiants
    ),
    path(
        'login/',
        login_view
    ),
    path(
        'generer_attestation/',
        generer_attestation,
        name='generer_attestation'
    ),

     path(
        'details-attestation/',
        details_attestation,
        name='details_attestation'
    ),

    path(
        'mes-attestations/',
        mes_attestations
    ),
    path(
        'login/',
        login_view
    ),

]