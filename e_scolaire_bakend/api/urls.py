from django.urls import path
from .views import register_etudiant

urlpatterns = [
    path('register/', register_etudiant, name='register'),
]