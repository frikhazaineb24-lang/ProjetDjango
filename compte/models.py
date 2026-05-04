from django.db import models
from django.contrib.auth.models import User

# Donneur
class Donneur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groupe_sanguin = models.CharField(max_length=5)
    sexe = models.CharField(max_length=10, choices=[('M','Masculin'),('F','Féminin')], default='M')
    date_naissance = models.DateField()
    ville = models.CharField(max_length=100)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}/{self.groupe_sanguin}/{self.ville}/{self.actif}"

# Hopital
class Hopital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    agrement = models.CharField(max_length=50)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom}/{self.adresse}/{self.ville}/{self.agrement}/{self.valide}"