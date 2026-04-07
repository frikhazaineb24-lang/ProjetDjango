from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # page d'accueil de l'app compte
]