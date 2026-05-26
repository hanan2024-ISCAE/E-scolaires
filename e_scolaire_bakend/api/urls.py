from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    DemandeInscriptionViewSet,
    MeView,
    MesNotesListView,
    ReclamationViewSet,
    RessourceViewSet,
    register_etudiant,
)

inscriptions_router = DefaultRouter()
inscriptions_router.register("demandes", DemandeInscriptionViewSet, basename="demande-inscription")

reclamations_router = DefaultRouter()
reclamations_router.register("", ReclamationViewSet, basename="reclamation")

ressources_router = DefaultRouter()
ressources_router.register("", RessourceViewSet, basename="ressource")

urlpatterns = [
    path("register/", register_etudiant, name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("inscriptions/", include(inscriptions_router.urls)),
    path("notes/mes/", MesNotesListView.as_view()),
    path("reclamations/", include(reclamations_router.urls)),
    path("ressources/", include(ressources_router.urls)),
]
