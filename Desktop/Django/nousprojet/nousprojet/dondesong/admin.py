from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import *

class DonneurAdmin(admin.ModelAdmin):
    list_display = ('user', 'groupe_sanguin', 'ville')

class HopitalAdmin(admin.ModelAdmin):

    list_display = ('nom', 'ville', 'valide', 'get_email')
    list_editable = ('valide',)

    def get_email(self, obj):
        # Récupère l'email lié au compte User de l'hôpital
        return obj.user.email
    get_email.short_description = 'Email'

    def save_model(self, request, obj, form, change):
        #Vérifie si on est en mode modification (et non création)
        ancien_obj = None
        if change:
            # Récupère l'ancien état
            ancien_obj = Hopital.objects.filter(id=obj.id).first()

        #Sauvegarde les modifications dans la bd
        super().save_model(request, obj, form, change)

        # Vérifie si l'hôpital vient d'être validé
        if ancien_obj and not ancien_obj.valide and obj.valide:
            try:
                #Sujet de l'email
                sujet = "✅ DonDeSang - Votre compte hôpital a été validé !"

                # 🔹 Contenu de l'email
                message = f"""
Bonjour {obj.user.username},

Félicitations ! Votre compte hôpital sur DonDeSang a été validé.

Vous pouvez maintenant :
- Créer des demandes urgentes de sang
- Organiser des campagnes de don
- Gérer votre espace hôpital

Connectez-vous ici :
http://127.0.0.1:8000/connexion/

Cordialement,
L'équipe DonDeSang
"""

                #Envoi de l'email
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,   # expéditeur
                    [obj.user.email],              # destinataire
                    fail_silently=False
                )

                #Message de succès dans l'admin Django
                self.message_user(
                    request,
                    f"Email de validation envoyé à {obj.user.email}"
                )

            except Exception as e:
                #En cas d'erreur lors de l'envoi email
                self.message_user(
                    request,
                    f"Erreur d'envoi d'email: {e}",
                    level='ERROR'
                )

class DemandeUrgenteAdmin(admin.ModelAdmin):
    list_display = ('hopital', 'groupe_sanguin', 'quantite', 'statut')

class DonAdmin(admin.ModelAdmin):
    list_display = ('donneur', 'hopital', 'date_don')

class CampagneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'hopital', 'date')

class CreneauAdmin(admin.ModelAdmin):
    list_display = ('campagne', 'heure_debut', 'heure_fin', 'capacite')

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('campagne', 'donneur', 'creneau', 'present')

class ReponseAppelAdmin(admin.ModelAdmin):
    list_display = ('demande', 'donneur', 'date_reponse', 'statut')

admin.site.register(Donneur, DonneurAdmin)
admin.site.register(Hopital, HopitalAdmin)
admin.site.register(DemandeUrgente, DemandeUrgenteAdmin)
admin.site.register(Don, DonAdmin)
admin.site.register(Campagne, CampagneAdmin)
admin.site.register(Creneau, CreneauAdmin)
admin.site.register(Inscription, InscriptionAdmin)
admin.site.register(ReponseAppel, ReponseAppelAdmin)