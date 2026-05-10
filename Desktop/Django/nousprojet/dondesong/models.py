from django.db import models
from django.contrib.auth.models import User

class Donneur(models.Model):
    GROUPE_SANGUIN_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    groupe_sanguin = models.CharField(
        max_length=3,
        choices=GROUPE_SANGUIN_CHOICES
    )

    sexe = models.CharField(
        max_length=1,
        choices=SEXE_CHOICES
    )

    date_naissance = models.DateField()

    ville = models.CharField(max_length=100)

    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.groupe_sanguin}"
    
class Hopital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nom = models.CharField(max_length=150)

    adresse = models.CharField(max_length=255)

    ville = models.CharField(max_length=100)

    agrement = models.CharField(max_length=100)

    valide = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

class DemandeUrgente(models.Model):

    GROUPE_SANGUIN_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée'),
        ('terminee', 'Terminée'),
    ]

    hopital = models.ForeignKey(
        'Hopital',
        on_delete=models.CASCADE,
        related_name='demandes_urgentes'
    )

    groupe_sanguin = models.CharField(
        max_length=3,
        choices=GROUPE_SANGUIN_CHOICES
    )

    quantite = models.IntegerField()

    delai = models.DateField()

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    description = models.TextField()

    def __str__(self):
        return f"{self.groupe_sanguin} - {self.hopital.nom}"
class Don(models.Model):

    donneur = models.ForeignKey(
        'Donneur',
        on_delete=models.CASCADE,
        related_name='dons'
    )

    hopital = models.ForeignKey(
        'Hopital',
        on_delete=models.CASCADE,
        related_name='dons'
    )

    date_don = models.DateField()

    notes = models.TextField(blank=True, null=True)

    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"Don de {self.donneur.user.username} - {self.date_don}"
class Campagne(models.Model):

    GROUPES_SANGUINS_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    hopital = models.ForeignKey('Hopital', on_delete=models.CASCADE, related_name='campagnes')

    nom = models.CharField(max_length=150)
    date = models.DateField()
    lieu = models.CharField(max_length=255)

    groupes_cibles = models.CharField(max_length=3, choices=GROUPES_SANGUINS_CHOICES)

    def __str__(self):
        return f"{self.nom} - {self.date}"
class Creneau(models.Model):

    campagne = models.ForeignKey(
        'Campagne',
        on_delete=models.CASCADE,
        related_name='creneaux'
    )

    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    capacite_max = models.IntegerField()

    def __str__(self):
        return f"{self.heure_debut} - {self.heure_fin}"
class Inscription(models.Model):

    creneau = models.ForeignKey(
        'Creneau',
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )

    donneur = models.ForeignKey(
        'Donneur',
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )

    date_inscription = models.DateTimeField(auto_now_add=True)

    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('creneau', 'donneur')

    def __str__(self):
        return f"{self.donneur.user.username} - {self.creneau}"
class ReponseAppel(models.Model):

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]

    demande = models.ForeignKey(
        'DemandeUrgente',
        on_delete=models.CASCADE,
        related_name='reponses'
    )

    donneur = models.ForeignKey(
        'Donneur',
        on_delete=models.CASCADE,
        related_name='reponses_appel'
    )

    date_reponse = models.DateTimeField(auto_now_add=True)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    def __str__(self):
        return f"{self.donneur.user.username} - {self.demande.groupe_sanguin} - {self.statut}"

