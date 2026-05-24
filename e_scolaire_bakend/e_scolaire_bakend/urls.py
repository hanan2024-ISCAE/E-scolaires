from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("api/auth/", include("users.urls_auth")),
    path("api/inscriptions/", include("users.urls_inscriptions")),
    path("api/notes/", include("notes.urls")),
    path("api/reclamations/", include("reclamations.urls")),
    path("api/ressources/", include("ressources.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
