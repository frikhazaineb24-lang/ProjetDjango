from django.db import models
from compte.models import Hopital, Donneur
from datetime import date

# Campagne
class Campagne(models.Model):
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    date = models.DateField(default=date.today)
    lieu = models.CharField(max_length=150)
    groupes_cibles = models.CharField(max_length=100)
    capacite_totale = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nom}/{self.hopital.nom}/{self.date}/{self.lieu}/{self.groupes_cibles}/{self.capacite_totale}"

# Inscription
class Inscription(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)
    donateur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    creneau_horaire = models.TimeField()
    date_inscription = models.DateField(default=date.today)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.donateur.user.username}/{self.campagne.nom}/{self.creneau_horaire}/{self.present}"