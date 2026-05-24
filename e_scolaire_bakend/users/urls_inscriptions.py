from rest_framework.routers import DefaultRouter

from .views import DemandeInscriptionViewSet

router = DefaultRouter()
router.register("demandes", DemandeInscriptionViewSet, basename="demande-inscription")

urlpatterns = router.urls
