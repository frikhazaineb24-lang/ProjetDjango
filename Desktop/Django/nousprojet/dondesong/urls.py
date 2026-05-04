from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('donneur/', views.donneurs_view, name='donneur'),
    path('hopitaux/', views.hopitaux_view, name='hopitaux'),
    path('campagnes/', views.campagnes_view, name='campagnes'),
    path('dons/', views.dons_view, name='dons'),
    path('demandes/', views.demandes_view, name='demandes'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('deconexion/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]
