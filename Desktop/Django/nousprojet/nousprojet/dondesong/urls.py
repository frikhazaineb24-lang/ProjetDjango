from django.urls import path
from . import views

urlpatterns = [
    # ───────────────────────
    # ACCUEIL
    # ───────────────────────
    path('', views.home, name='home'),

    # ───────────────────────
    # AUTHENTIFICATION
    # ───────────────────────
    path('inscription/donneur/', views.inscription_donneur, name='inscription_donneur'),
    path('inscription/hopital/', views.inscription_hopital, name='inscription_hopital'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    # ───────────────────────
    # DONNEUR
    # ───────────────────────
    path('donneur/', views.dashboard_donneur, name='dashboard_donneur'),
    path('repondre/<int:id>/', views.repondre_demande, name='repondre'),
    path('enregistrer-don/', views.enregistrer_don, name='enregistrer_don'),
    path('donneur/historique/', views.historique_dons, name='historique_dons'),
    path('donneur/profil/', views.modifier_profil_donneur, name='modifier_profil_donneur'),


    # ───────────────────────
    # HÔPITAL
    # ───────────────────────
    path('hopital/', views.dashboard_hopital, name='dashboard_hopital'),
    path('demande/ajouter/', views.ajouter_demande, name='ajouter_demande'),
    path('demande/<int:id>/modifier/', views.modifier_demande, name='modifier_demande'),
    path('demande/<int:id>/cloturer/', views.cloturer_demande, name='cloturer_demande'),
    path('demande/<int:id>/reponses/', views.voir_reponses, name='voir_reponses'),
    path('historique/', views.historique_demandes, name='historique_demandes'),
    path('hopital/profil/', views.modifier_profil_hopital, name='modifier_profil_hopital'),


    # ───────────────────────
    # CAMPAGNES
    # ───────────────────────
    path('campagnes/', views.liste_campagnes, name='liste_campagnes'),
    path('campagnes/creer/', views.creer_campagne, name='creer_campagne'),
    path('campagnes/<int:campagne_id>/inscription/', views.inscription_campagne, name='inscription_campagne'),
    path('mes-inscriptions/', views.mes_inscriptions, name='mes_inscriptions'),
    path('mes-inscriptions/<int:inscription_id>/annuler/', views.annuler_inscription, name='annuler_inscription'),
    path('campagne/<int:campagne_id>/details/', views.details_campagne, name='details_campagne'),

    # ───────────────────────
    # ADMIN
    # ───────────────────────
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('valider-hopital/<int:hopital_id>/', views.valider_hopital, name='valider_hopital'),
    path('export-donneurs-csv/', views.export_donneurs_csv, name='export_donneurs_csv'),
]