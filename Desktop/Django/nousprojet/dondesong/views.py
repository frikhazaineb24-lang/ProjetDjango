from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from datetime import timedelta, date
from django.contrib import messages

from .models import (
    Donneur, Hopital, DemandeUrgente, Don,
    Campagne, Inscription, ReponseAppel, Creneau 
)

from .forms import (
    DonneurForm, HopitalForm, DemandeUrgenteForm,
    DonForm, CampagneForm, InscriptionForm,
    ReponseAppelForm, UserRegistrationForm
)

# ---------- INDEX ----------
def index(request):
    return render(request, 'dondesong/index.html')


# ---------- DONNEUR ----------
@login_required
def donneurs_view(request):
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
    hopital = Hopital.objects.filter(user=request.user).first()

    if not hopital:
        messages.error(request, "Vous devez être hôpital.")
        return redirect('index')

    if request.method == 'POST':
        form = DemandeUrgenteForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.hopital = hopital
            demande.save()
            messages.success(request, "Demande créée.")
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
        messages.error(request, "Profil donneur requis.")
        return redirect('index')

    if request.method == 'POST':
        form = DonForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            don.donneur = donneur
            don.save()
            messages.success(request, "Don enregistré.")
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
        messages.error(request, "Seul hôpital peut créer campagne.")
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


# ---------- INSCRIPTION CAMPAGNE ----------
@login_required
def inscriptions_view(request):
    donneur = Donneur.objects.filter(user=request.user).first()

    if not donneur:
        messages.error(request, "Vous devez être donneur.")
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

    inscriptions = Inscription.objects.filter(donneur=donneur)

    return render(request, 'dondesong/inscriptions.html', {
        'form': form,
        'inscriptions': inscriptions
    })


# ---------- RÉPONSES ----------
@login_required
def reponses_view(request):
    donneur = Donneur.objects.filter(user=request.user).first()

    if not donneur:
        messages.error(request, "Donneur requis.")
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

    reponses = ReponseAppel.objects.filter(donneur=donneur)

    return render(request, 'dondesong/reponses.html', {
        'form': form,
        'reponses': reponses
    })


# ---------- REGISTER ----------
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, f'Bienvenue {username}')
            return redirect('index')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


# ---------- DASHBOARD DONNEUR ----------
@login_required
def dashboard_donneur(request):
    donneur = request.user.donneur

    dons = Don.objects.filter(donneur=donneur).order_by('-date_don')
    dernier_don = dons.first()

    delai = 56 if donneur.sexe == 'M' else 84

    if dernier_don:
        prochaine_date = dernier_don.date_don + timedelta(days=delai)
    else:
        prochaine_date = date.today()

    demandes = DemandeUrgente.objects.filter(
        groupe_sanguin=donneur.groupe_sanguin,
        statut='en_attente'
    )

    return render(request, 'dondesong/dashboard.html', {
        'dons': dons,
        'prochaine_date': prochaine_date,
        'demandes': demandes,
        'donneur': donneur
    })


# ---------- RÉPONDRE APPEL ----------
@login_required
def repondre_appel(request, id):
    demande = DemandeUrgente.objects.get(id=id)
    donneur = request.user.donneur

    ReponseAppel.objects.create(
        demande=demande,
        donneur=donneur,
        statut='accepte'
    )

    return redirect('dashboard_donneur')


# ---------- AJOUT DON ----------
@login_required
def ajouter_don(request, id):
    donneur = request.user.donneur
    hopital = Hopital.objects.get(id=id)

    Don.objects.create(
        donneur=donneur,
        hopital=hopital,
        date_don=date.today(),
        valide=True
    )

    return redirect('dashboard_donneur')


# ---------- CRENEAUX ----------
def creneau_list(request):
    creneaux = Creneau.objects.all()
    return render(request, 'dondesong/creneaux.html', {'creneaux': creneaux})


def creneau_detail(request, id):
    campagne = Campagne.objects.get(id=id)
    creneaux = campagne.creneaux.all()

    return render(request, 'dondesong/creneaux.html', {
        'campagne': campagne,
        'creneaux': creneaux
    })


# ---------- INSCRIPTION CRENEAU ----------
@login_required
def inscription_creneau(request, id):
    creneau = Creneau.objects.get(id=id)

    if creneau.inscriptions.count() >= creneau.capacite_max:
        return render(request, 'dondesong/full.html')

    Inscription.objects.create(
        creneau=creneau,
        donneur=request.user.donneur
    )

    return redirect('dashboard_donneur')