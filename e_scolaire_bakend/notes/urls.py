from django.urls import path

from .views import MesNotesListView

urlpatterns = [path("mes/", MesNotesListView.as_view())]
