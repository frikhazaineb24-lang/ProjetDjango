from django.db import models
from compte.models import Donneur, Hopital
from hopital.models import DemandeUrgente
from datetime import date

# Don
class Don(models.Model):
    donateur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    date_don = models.DateField(default=date.today)
    notes = models.TextField(blank=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.donateur.user.username}/{self.hopital.nom}/{self.date_don}/{self.valide}"

# Réponse à un appel urgent
class ReponseAppel(models.Model):
    demande = models.ForeignKey(DemandeUrgente, on_delete=models.CASCADE)
    donateur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    date_reponse = models.DateField(default=date.today)
    statut = models.CharField(max_length=20, choices=[('accepte','Accepté'),('refuse','Refusé')], default='accepte')

    def __str__(self):
        return f"{self.donateur.user.username}/{self.demande.hopital.nom}/{self.statut}/{self.date_reponse}"