from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import (
    Donneur, Hopital, DemandeUrgente, Don,
    Campagne, Inscription, ReponseAppel
)
from .forms import (
    DonneurForm, HopitalForm, DemandeUrgenteForm,
    DonForm, CampagneForm, InscriptionForm, ReponseAppelForm,
    UserRegistrationForm
)


# ---------- INDEX ----------
def index(request):
    return render(request, 'dondesong/index.html')


# ---------- DONNEUR ----------
@login_required
def donneurs_view(request):
    # Récupère le profil donneur de l'utilisateur connecté (s'il existe)
    donneur_existant = Donneur.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = DonneurForm(request.POST, instance=donneur_existant)
        if form.is_valid():
            donneur = form.save(commit=False)
            donneur.user = request.user
            donneur.save()
            messages.success(request, "Profil donneur enregistré avec succès !")
            return redirect('donneur')
    else:
        form = DonneurForm(instance=donneur_existant)

    donneur = Donneur.objects.all()
    return render(request, 'dondesong/donneur.html', {
        'form': form,
        'donneur': donneur
    })


# ---------- HÔPITAL ----------
@login_required
def hopitaux_view(request):
    hopital_existant = Hopital.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = HopitalForm(request.POST, instance=hopital_existant)
        if form.is_valid():
            hopital = form.save(commit=False)
            hopital.user = request.user
            hopital.save()
            messages.success(request, "Hôpital enregistré avec succès !")
            return redirect('hopitaux')
    else:
        form = HopitalForm(instance=hopital_existant)

    hopitaux = Hopital.objects.filter(valide=True)
    return render(request, 'dondesong/hopitaux.html', {
        'form': form,
        'hopitaux': hopitaux
    })


# ---------- DEMANDE URGENTE ----------
@login_required
def demandes_view(request):
    # Seul un hôpital peut créer une demande urgente
    hopital = Hopital.objects.filter(user=request.user).first()
    if not hopital:
        messages.error(request, "Vous devez être enregistré comme hôpital pour créer une demande.")
        return redirect('index')

    if request.method == 'POST':
        form = DemandeUrgenteForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.hopital = hopital
            demande.save()
            messages.success(request, "Demande urgente créée.")
            return redirect('demandes')
    else:
        form = DemandeUrgenteForm()

    demandes = DemandeUrgente.objects.all().order_by('-delai')
    return render(request, 'dondesong/demandes.html', {
        'form': form,
        'demandes': demandes
    })


# ---------- DON ----------
@login_required
def dons_view(request):
    donneur = Donneur.objects.filter(user=request.user).first()
    if not donneur:
        messages.error(request, "Vous devez avoir un profil donneur pour enregistrer un don.")
        return redirect('index')

    if request.method == 'POST':
        form = DonForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            don.donneur = donneur
            don.save()
            messages.success(request, "Don enregistré avec succès.")
            return redirect('dons')
    else:
        form = DonForm()

    dons = Don.objects.filter(donneur=donneur).order_by('-date_don')
    return render(request, 'dondesong/dons.html', {
        'form': form,
        'dons': dons
    })


# ---------- CAMPAGNE ----------
@login_required
def campagnes_view(request):
    hopital = Hopital.objects.filter(user=request.user).first()
    if not hopital:
        messages.error(request, "Seul un hôpital peut créer une campagne.")
        return redirect('index')

    if request.method == 'POST':
        form = CampagneForm(request.POST)
        if form.is_valid():
            campagne = form.save(commit=False)
            campagne.hopital = hopital
            campagne.save()
            messages.success(request, "Campagne créée.")
            return redirect('campagnes')
    else:
        form = CampagneForm()

    campagnes = Campagne.objects.all().order_by('-date')
    return render(request, 'dondesong/campagnes.html', {
        'form': form,
        'campagnes': campagnes
    })


# ---------- INSCRIPTION À UNE CAMPAGNE ----------
@login_required
def inscriptions_view(request):
    donneur = Donneur.objects.filter(user=request.user).first()
    if not donneur:
        messages.error(request, "Vous devez être donneur pour vous inscrire.")
        return redirect('index')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            inscription = form.save(commit=False)
            inscription.donneur = donneur
            inscription.save()
            messages.success(request, "Inscription réussie.")
            return redirect('inscriptions')
    else:
        form = InscriptionForm()

    inscriptions = Inscription.objects.filter(donneur=donneur).order_by('-date_inscription')
    return render(request, 'dondesong/inscriptions.html', {
        'form': form,
        'inscriptions': inscriptions
    })


# ---------- RÉPONSE À UN APPEL ----------
@login_required
def reponses_view(request):
    donneur = Donneur.objects.filter(user=request.user).first()
    if not donneur:
        messages.error(request, "Seul un donneur peut répondre à un appel.")
        return redirect('index')

    if request.method == 'POST':
        form = ReponseAppelForm(request.POST)
        if form.is_valid():
            reponse = form.save(commit=False)
            reponse.donneur = donneur
            reponse.save()
            messages.success(request, "Réponse envoyée.")
            return redirect('reponses')
    else:
        form = ReponseAppelForm()

    reponses = ReponseAppel.objects.filter(donneur=donneur).order_by('-date_reponse')
    return render(request, 'dondesong/reponses.html', {
        'form': form,
        'reponses': reponses
    })


# ---------- INSCRIPTION UTILISATEUR ----------
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Bienvenue {username}, votre compte a été créé !')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})