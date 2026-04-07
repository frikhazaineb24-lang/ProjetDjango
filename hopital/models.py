from django.db import models
from compte.models import Hopital

# Demande urgente
class DemandeUrgente(models.Model):
    STATUT_CHOICES = [('en_attente','En attente'),('valide','Validé'),('refuse','Refusé')]
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    groupe_sanguin = models.CharField(max_length=5)
    quantite = models.PositiveIntegerField()
    delai = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    description = models.TextField(default='')

    def __str__(self):
        return f"{self.hopital.nom}/{self.groupe_sanguin}/{self.quantite}/{self.statut}"