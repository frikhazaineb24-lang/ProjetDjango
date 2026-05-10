from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import (
    Donneur, Hopital, DemandeUrgente, Don,
    Campagne, Inscription, ReponseAppel, Creneau
)


# ---------- DONNEUR ----------
class DonneurForm(forms.ModelForm):
    class Meta:
        model = Donneur
        fields = ['groupe_sanguin', 'sexe', 'date_naissance', 'ville', 'actif']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'groupe_sanguin': forms.Select(attrs={'class': 'form-select'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ---------- HÔPITAL ----------
class HopitalForm(forms.ModelForm):
    class Meta:
        model = Hopital
        fields = ['nom', 'adresse', 'ville', 'agrement']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'agrement': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ---------- DEMANDE URGENTE ----------
class DemandeUrgenteForm(forms.ModelForm):
    class Meta:
        model = DemandeUrgente
        fields = ['groupe_sanguin', 'quantite', 'delai', 'description']
        widgets = {
            'delai': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'groupe_sanguin': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ---------- DON ----------
class DonForm(forms.ModelForm):
    class Meta:
        model = Don
        fields = ['hopital', 'date_don', 'notes']
        widgets = {
            'date_don': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hopital': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ---------- CAMPAGNE ----------
class CampagneForm(forms.ModelForm):
    class Meta:
        model = Campagne
        fields = ['nom', 'lieu', 'date', 'groupes_cibles']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
            'groupes_cibles': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ---------- INSCRIPTION (CORRIGÉ) ----------
class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['creneau']   # ✔ SEULEMENT CE CHAMP
        widgets = {
            'creneau': forms.Select(attrs={'class': 'form-select'}),
        }


# ---------- RÉPONSE APPEL ----------
class ReponseAppelForm(forms.ModelForm):
    class Meta:
        model = ReponseAppel
        fields = ['demande']
        widgets = {
            'demande': forms.Select(attrs={'class': 'form-select'}),
        }


# ---------- USER ----------
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'