from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, ReclamationViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'reclamations', ReclamationViewSet, basename='reclamation')

urlpatterns = [
    path('', include(router.urls)),
]