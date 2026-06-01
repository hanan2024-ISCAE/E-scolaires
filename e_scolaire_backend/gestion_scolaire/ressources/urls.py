from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RessourcePedagogiqueViewSet

router = DefaultRouter()
router.register(r'ressources', RessourcePedagogiqueViewSet, basename='ressource')

urlpatterns = [
    path('', include(router.urls)),
]