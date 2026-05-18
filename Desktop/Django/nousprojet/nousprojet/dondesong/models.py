from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class Donneur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groupe_sanguin = models.CharField(max_length=3)
    sexe = models.CharField(max_length=1, choices=[('H', 'Homme'), ('F', 'Femme')])
    date_naissance = models.DateField()
    ville = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    actif = models.BooleanField(default=True) 
    def dernier_don(self):
        return Don.objects.filter(donneur=self).order_by('-date_don').first()
#prochaine date qui le donneur peut faire un don en fonction de son sexe et de la date de son dernier don
    def date_prochain_don(self):
        dernier = self.dernier_don()
        if not dernier:
            return date.today()
        delai = 56 if self.sexe == 'H' else 84
        return dernier.date_don + timedelta(days=delai)
#fonction qui vérifie si le donneur peut donner un don aujourd'hui
    def est_eligible(self):
        return date.today() >= self.date_prochain_don()
#fonction qui retourne le nombre de jours restants avant le prochain don
    def jours_restants(self):
        """Retourne le nombre de jours restants avant le prochain don"""
        prochain = self.date_prochain_don()
        if prochain > date.today():
            return (prochain - date.today()).days
        return 0

class Hopital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    ville = models.CharField(max_length=50)
    agrement = models.CharField(max_length=50)
    valide = models.BooleanField(default=False)


class DemandeUrgente(models.Model):
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    groupe_sanguin = models.CharField(max_length=3)
    quantite = models.IntegerField()
    delai = models.DateField()
    statut = models.CharField(max_length=20, default='active')
    description = models.TextField()
#fonction qui vérifie si la demande urgente est expirée en fonction du delai
    def est_expire(self):
        return self.delai < date.today()


class Don(models.Model):
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    date_don = models.DateField()
    notes = models.TextField(blank=True)
    valide = models.BooleanField(default=True)


class Campagne(models.Model):
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    date = models.DateField()
    lieu = models.CharField(max_length=100)
    groupes_cibles = models.CharField(max_length=50)
    capacite_totale = models.IntegerField()


class Creneau(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    capacite = models.IntegerField()


class Inscription(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    creneau = models.ForeignKey(Creneau, on_delete=models.CASCADE, null=True, blank=True)
    date_inscription = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=False)


class ReponseAppel(models.Model):
    demande = models.ForeignKey(DemandeUrgente, on_delete=models.CASCADE)
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    date_reponse = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[
        ('intention', 'Intention'),
        ('effectue', 'Effectué')
    ])
#un même donneur ne peut répondre qu’une seule fois à la même demande urgente.
#unique emch
    class Meta:
        unique_together = ('demande', 'donneur')