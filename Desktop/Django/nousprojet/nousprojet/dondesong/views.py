from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from datetime import date, datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from django.db.models import Count
import csv
from django.http import HttpResponse
#Cette fonction est un décorateur personnalisé pour vérifier si l'utilisateur est connecté avant d'accéder à certaines vues. Si l'utilisateur n'est pas authentifié, il est redirigé vers la page de connexion.
def login_required_dondesong(view_func):
    def wrapper(request, *args, **kwargs):# recevoir la requête et les arguments de la vue décorée
        if not request.user.is_authenticated:
            return redirect('connexion')
        return view_func(request, *args, **kwargs)#
    wrapper.__name__ = view_func.__name__
    return wrapper

def inscription_donneur(request):
    groupes = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        prenom = request.POST['prenom'].strip()
        nom = request.POST['nom'].strip()
        groupe = request.POST['groupe_sanguin']
        sexe = request.POST['sexe']
        naissance = request.POST['date_naissance']
        ville = request.POST['ville'].strip()
        telephone = request.POST.get('telephone', '').strip()

        if not all([username, email, password, prenom, nom, groupe, sexe, naissance, ville]):
            return render(request, 'registration/inscriptiondonneur.html', {
                'groupes': groupes, 'erreur': "Tous les champs obligatoires doivent être remplis."
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/inscriptiondonneur.html', {'groupes': groupes, 'erreur': "Ce nom d'utilisateur existe déjà."})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'registration/inscriptiondonneur.html', {'groupes': groupes, 'erreur': "Cet email est déjà utilisé."})

        user = User.objects.create_user(username=username, email=email, password=password, first_name=prenom, last_name=nom)
        Donneur.objects.create(user=user, groupe_sanguin=groupe, sexe=sexe, date_naissance=naissance, ville=ville, telephone=telephone)
        
        try:
            send_mail('Bienvenue sur DonDeSang', f'Bonjour {prenom} {nom},\n\nVotre compte donneur a été créé avec succès !', settings.DEFAULT_FROM_EMAIL, [email], fail_silently=True)
        except:
            pass
        
        login(request, user)
        messages.success(request, f"Bienvenue {prenom} !")
        return redirect('dashboard_donneur')

    return render(request, 'registration/inscriptiondonneur.html', {'groupes': groupes})

def inscription_hopital(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        nom = request.POST['nom'].strip()
        adresse = request.POST['adresse'].strip()
        ville = request.POST['ville'].strip()
        agrement = request.POST['agrement'].strip()

        if not all([username, email, password, nom, adresse, ville, agrement]):
            return render(request, 'registration/inscriptionhopital.html', {'erreur': "Tous les champs sont obligatoires."})

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/inscriptionhopital.html', {'erreur': "Ce nom d'utilisateur existe déjà."})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'registration/inscriptionhopital.html', {'erreur': "Cet email est déjà utilisé."})

        user = User.objects.create_user(username=username, email=email, password=password)
        Hopital.objects.create(user=user, nom=nom, adresse=adresse, ville=ville, agrement=agrement, valide=False)
        
        try:
            send_mail('Votre compte hôpital est en attente de validation', 
                     f'Bonjour {nom},\n\nVotre compte a été créé avec succès.\n\nIl est actuellement en attente de validation par un administrateur.\n\nVous recevrez un email de confirmation dès que votre compte sera validé.\n\nCordialement,\nL\'équipe DonDeSang', 
                     settings.DEFAULT_FROM_EMAIL, [email], fail_silently=True)
        except:
            pass
        
        login(request, user)
        messages.info(request, "Compte créé. En attente de validation.")
        return redirect('dashboard_hopital')

    return render(request, 'registration/inscriptionhopital.html')

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if Donneur.objects.filter(user=user).exists():
                return redirect('dashboard_donneur')
            elif Hopital.objects.filter(user=user).exists():
                return redirect('dashboard_hopital')
            return redirect('home')
        return render(request, 'registration/connexion.html', {'erreur': "Identifiants incorrects."})
    return render(request, 'registration/connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')

def home(request):
    is_donneur = False
    is_hopital = False
    if request.user.is_authenticated:
        is_donneur = Donneur.objects.filter(user=request.user).exists()
        is_hopital = Hopital.objects.filter(user=request.user).exists()
    return render(request, 'dondesong/index.html', {'is_donneur': is_donneur, 'is_hopital': is_hopital})

# ──────────────────────────────────────────
# DONNEUR
# ──────────────────────────────────────────

@login_required_dondesong
def dashboard_donneur(request):
    donneur = Donneur.objects.filter(user=request.user).first()
    dons = []
    demandes = []
    prochaine_date = ""
    eligible = False
    jours_restants = 0

    if donneur:
        dons = Don.objects.filter(donneur=donneur)
        compatibilite = {
            'O-': ['O-'], 'O+': ['O+', 'O-'], 'A+': ['A+', 'A-', 'O+', 'O-'],
            'A-': ['A-', 'O-'], 'B+': ['B+', 'B-', 'O+', 'O-'], 'B-': ['B-', 'O-'],
            'AB+': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
            'AB-': ['AB-', 'A-', 'B-', 'O-']
        }
        groupes_compatibles = compatibilite.get(donneur.groupe_sanguin, [])
        demandes = DemandeUrgente.objects.filter(statut='active', groupe_sanguin__in=groupes_compatibles)
        prochaine_date = donneur.date_prochain_don()
        eligible = donneur.est_eligible()
        jours_restants = donneur.jours_restants()

    return render(request, "donneur/dashboarddonneur.html", {
        "donneur": donneur, "dons": dons, "demandes": demandes,
        "prochaine_date": prochaine_date, "eligible": eligible, "jours_restants": jours_restants
    })

@login_required_dondesong
def repondre_demande(request, id):
    donneur = Donneur.objects.filter(user=request.user).first()
    if donneur:
        demande = DemandeUrgente.objects.get(id=id)
        if donneur.est_eligible():
            if not ReponseAppel.objects.filter(demande=demande, donneur=donneur).exists():
                ReponseAppel.objects.create(demande=demande, donneur=donneur, statut='intention')
                messages.success(request, " Votre réponse a été envoyée.")
            else:
                messages.warning(request, "Vous avez déjà répondu.")
        else:
            messages.error(request, "Vous n'êtes pas éligible.")
    return redirect('dashboard_donneur')

@login_required_dondesong
def enregistrer_don(request):
    donneur = Donneur.objects.filter(user=request.user).first()
    if not donneur:
        messages.error(request, "Compte donneur introuvable.")
        return redirect('dashboard_donneur')
    if request.method == 'POST':
        hopital_id = request.POST.get('hopital')
        hopital = Hopital.objects.get(id=hopital_id)
        Don.objects.create(donneur=donneur, hopital=hopital, date_don=date.today())
        messages.success(request, " Don enregistré !")
        return redirect('dashboard_donneur')
    hopitaux = Hopital.objects.filter(valide=True)
    return render(request, 
                  'donneur/enregistrerdonneur.html', {'hopitaux': hopitaux, 'aujourdhui': date.today()})

# HÔPITAL
@login_required_dondesong
def dashboard_hopital(request):
    hopital = Hopital.objects.filter(user=request.user).first()
    if not hopital:
        messages.error(request, "Vous n'avez pas de compte hôpital.")
        return redirect('inscription_hopital')
    if not hopital.valide:
        messages.warning(request, "Compte en attente de validation.")
        return render(request, "hopital/validationattente.html", {"hopital": hopital})
    demandes = DemandeUrgente.objects.filter(hopital=hopital)
    campagnes = Campagne.objects.filter(hopital=hopital)
    return render(request, "hopital/dashboardhopital.html", {
        "hopital": hopital, "demandes": demandes, "campagnes": campagnes
    })

from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required_dondesong
def ajouter_demande(request):
    hopital = Hopital.objects.filter(user=request.user).first()
    groupes = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]

    if request.method == 'POST' and hopital:
        delai = request.POST['delai']

        # تحويل النص إلى date
        try:
            delai_date = date.fromisoformat(delai)
        except ValueError:
            messages.error(request, "Date invalide.")
            return render(request, 'hopital/ajouterdemande.html', {'groupes': groupes})

        # Vérification date passée
        if delai_date < date.today():
            messages.error(request, "La date ne peut pas être inférieure à la date d'aujourd'hui.")
            return render(request, 'hopital/ajouterdemande.html', {'groupes': groupes})

        DemandeUrgente.objects.create(
            hopital=hopital,
            groupe_sanguin=request.POST['groupe'],
            quantite=request.POST['quantite'],
            delai=delai_date,
            description=request.POST['description']
        )

        messages.success(request, "Demande ajoutée.")
        return redirect('dashboard_hopital')

    return render(request, 'hopital/ajouterdemande.html', {'groupes': groupes})

@login_required_dondesong
def modifier_demande(request, id):
    demande = DemandeUrgente.objects.get(id=id)
    if request.method == 'POST':
        demande.quantite = request.POST.get('quantite')
        demande.delai = request.POST.get('delai')
        demande.description = request.POST.get('description')
        demande.save()
        messages.success(request, "Demande modifiée.")
        return redirect('dashboard_hopital')
    return render(request, 'hopital/modifdemande.html', {'demande': demande})

@login_required_dondesong
def cloturer_demande(request, id):
    demande = DemandeUrgente.objects.get(id=id)
    demande.statut = 'cloture'
    demande.save()
    messages.success(request, "Demande clôturée.")
    return redirect('dashboard_hopital')

@login_required_dondesong
def voir_reponses(request, id):
    demande = DemandeUrgente.objects.get(id=id)
    reponses = ReponseAppel.objects.filter(demande=demande)
    return render(request, 'hopital/reponses.html', {'demande': demande, 'reponses': reponses})

@login_required_dondesong
def historique_demandes(request):
    hopital = Hopital.objects.filter(user=request.user).first()
    if not hopital:
        return redirect('dashboard_donneur')
    demandes = DemandeUrgente.objects.filter(hopital=hopital).order_by('-id')
    return render(request, 'hopital/historique.html', {'demandes': demandes})

@login_required_dondesong
def modifier_profil_hopital(request):
    hopital = Hopital.objects.filter(user=request.user).first()
    if not hopital:
        return redirect('dashboard_donneur')
    if request.method == 'POST':
        hopital.nom = request.POST.get('nom')
        hopital.adresse = request.POST.get('adresse')
        hopital.ville = request.POST.get('ville')
        hopital.save()
        messages.success(request, "Profil mis à jour.")
        return redirect('dashboard_hopital')
    return render(request, 'hopital/modifprofil.html', {'hopital': hopital})
# PROFILS DONNEUR
@login_required_dondesong
def modifier_profil_donneur(request):
    donneur = Donneur.objects.filter(user=request.user).first()
    if not donneur:
        return redirect('dashboard_hopital')
    if request.method == 'POST':
        donneur.ville = request.POST.get('ville')
        donneur.telephone = request.POST.get('telephone')
        donneur.save()
        messages.success(request, "Profil mis à jour.")
        return redirect('dashboard_donneur')
    return render(request, 'donneur/modifierprofil.html', {'donneur': donneur})
# CAMPAGNES

@login_required_dondesong
def liste_campagnes(request):
    donneur = Donneur.objects.filter(user=request.user).first()
    if not donneur:
        return redirect('dashboard_hopital')
    campagnes = Campagne.objects.filter(date__gte=date.today()).order_by('date')
    deja_inscrit_ids = list(Inscription.objects.filter(donneur=donneur).values_list('campagne_id', flat=True))
    return render(request, 'campagnes/listecam.html', {'campagnes': campagnes, 'deja_inscrit_ids': deja_inscrit_ids})
@login_required_dondesong
def inscription_campagne(request, campagne_id):
    donneur = Donneur.objects.filter(user=request.user).first()
    if not donneur:
        return redirect('dashboard_hopital')
    campagne = Campagne.objects.get(id=campagne_id)
    creneaux = campagne.creneau_set.all()
    eligible = donneur.est_eligible()
    prochaine_date = donneur.date_prochain_don() if not eligible else None
    if Inscription.objects.filter(donneur=donneur, campagne=campagne).exists():
        messages.warning(request, "Déjà inscrit.")
        return redirect('liste_campagnes')
    if request.method == 'POST':
        if not eligible:
            messages.error(request, "Non éligible.")
            return redirect('liste_campagnes')
        
        creneau_id = request.POST.get('creneau')
        
     
        if not creneau_id:
            messages.error(request, "Veuillez sélectionner un créneau.")
            return redirect('inscription_campagne', campagne_id=campagne_id)
    
        
        creneau = get_object_or_404(Creneau, id=creneau_id)
        
        if creneau.inscription_set.count() >= creneau.capacite:
            messages.error(request, "Créneau complet.")
        else:
            Inscription.objects.create(donneur=donneur, campagne=campagne, creneau=creneau)
            messages.success(request, "Inscription réussie.")
            return redirect('mes_inscriptions')
    return render(request, 'campagnes/inscriptioncam.html', {
        'campagne': campagne, 'creneaux': creneaux, 'eligible': eligible, 'prochaine_date': prochaine_date
    })
from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
# Vérifie que l'utilisateur est connecté avant d'accéder à cette fonction
@login_required_dondesong

# Fonction pour créer une campagne de don de sang
def creer_campagne(request):

    # Récupère l'hôpital lié à l'utilisateur connecté
    hopital = Hopital.objects.filter(user=request.user).first()

    # Si aucun hôpital n'est trouvé
    if not hopital:

        # Redirige vers le tableau de bord donneur
        return redirect('dashboard_donneur')

    # Vérifie si le compte hôpital est validé
    if not hopital.valide:

        # Affiche un message d'erreur
        messages.error(request, "Compte non validé.")

        # Redirige vers le dashboard hôpital
        return redirect('dashboard_hopital')

    # Liste des groupes sanguins disponibles
    groupes = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]

    # Vérifie si le formulaire a été envoyé
    if request.method == 'POST':
        nom = request.POST.get('nom')
        date_campagne = request.POST.get('date')
        lieu = request.POST.get('lieu')
        capacite_totale = request.POST.get('capacite_totale')
        try:

            # Conversion du texte en objet date
            date_obj = date.fromisoformat(date_campagne)
        except ValueError:
            messages.error(request, "Date invalide.")

                # Recharge la page
            return render(
                request,
                'campagnes/creercam.html',
                {'groupes': groupes}
            )

        # Vérifie si la date est passée
        if date_obj < date.today():

            # Message erreur
            messages.error(
                request,
                "La date de la campagne ne peut pas être dans le passé."
            )

            # Retourne vers le formulaire
            return render(
                request,
                'campagnes/creercam.html',
                {'groupes': groupes}
            )

        # Récupère les groupes sanguins sélectionnés
        # puis les transforme en texte
        groupes_cibles = " ".join(
            request.POST.getlist('groupes_cibles')
        ) or "Tous"

        # Création de la campagne dans la base de données
        campagne = Campagne.objects.create(
            hopital=hopital,
            nom=nom,
            date=date_obj,
            lieu=lieu,
            capacite_totale=int(capacite_totale),
            groupes_cibles=groupes_cibles
        )

        # Liste des heures de début des créneaux
        heures_debut = request.POST.getlist('heure_debut[]')

        # Liste des heures de fin des créneaux
        heures_fin = request.POST.getlist('heure_fin[]')

        # Liste des capacités des créneaux
        capacites = request.POST.getlist('capacite_creneau[]')

        # Boucle sur tous les créneaux
        for i in range(len(heures_debut)):

            # Vérifie que les heures existent
            if heures_debut[i] and heures_fin[i]:

                # Création du créneau
                Creneau.objects.create(

                    # Créneau lié à la campagne
                    campagne=campagne,

                    # Heure de début
                    heure_debut=heures_debut[i],

                    # Heure de fin
                    heure_fin=heures_fin[i],

                    # Nombre maximal de donneurs
                    capacite=int(capacites[i])
                    if i < len(capacites)
                    else 10
                )

        # Message succès après création
        messages.success(
            request,
            f"Campagne '{nom}' créée !"
        )

        # Redirection vers dashboard hôpital
        return redirect('dashboard_hopital')

    return render(request, 'campagnes/creercam.html', {'groupes': groupes})
@login_required_dondesong
def mes_inscriptions(request):
    donneur = Donneur.objects.filter(user=request.user).first()
    if not donneur:
        return redirect('dashboard_hopital')
    inscriptions = Inscription.objects.filter(donneur=donneur).select_related('campagne').order_by('-campagne__date')
    return render(request, 'campagnes/mesinscriptions.html', {'inscriptions': inscriptions, 'aujourd_hui': date.today()})

@login_required_dondesong
def annuler_inscription(request, inscription_id):
    donneur = Donneur.objects.filter(user=request.user).first()
    if not donneur:
        return redirect('dashboard_hopital')
    inscription = Inscription.objects.filter(id=inscription_id, donneur=donneur).first()
    if inscription:
        inscription.delete()
        messages.success(request, "Inscription annulée.")
    else:
        messages.error(request, "Inscription introuvable.")
    return redirect('mes_inscriptions')
@login_required_dondesong
def details_campagne(request, campagne_id):
    
    hopital = Hopital.objects.filter(user=request.user).first()
    if not hopital:
        messages.error(request, "Accès réservé aux hôpitaux.")
        return redirect('dashboard_donneur')
    campagne = get_object_or_404(Campagne, id=campagne_id, hopital=hopital)
    
    inscriptions = Inscription.objects.filter(campagne=campagne).select_related('donneur', 'creneau')
    inscriptions_par_creneau = {}
    for creneau in campagne.creneau_set.all():
        count = Inscription.objects.filter(campagne=campagne, creneau=creneau).count()
        inscriptions_par_creneau[creneau] = count
    
    return render(request, 'hopital/detailscam.html', {
        'campagne': campagne,
        'inscriptions': inscriptions,
        'inscriptions_par_creneau': inscriptions_par_creneau,
        'total_inscrits': inscriptions.count()
    })
# ADMINISTRATION
@login_required_dondesong
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('home')
    

    
    total_donneurs = Donneur.objects.count()
    total_hopitaux = Hopital.objects.count()
    hopitaux_non_valides = Hopital.objects.filter(valide=False).count()
    hopitaux_valides = Hopital.objects.filter(valide=True)  
    total_dons = Don.objects.count()
    demandes_actives = DemandeUrgente.objects.filter(statut='active').count()
    campagnes_a_venir = Campagne.objects.filter(date__gte=date.today()).count()
    hopitaux_attente = Hopital.objects.filter(valide=False)
    demandes_par_groupe = DemandeUrgente.objects.filter(statut='active').values('groupe_sanguin').annotate(total=Count('id'))
    demandes_par_ville = DemandeUrgente.objects.filter(statut='active').select_related('hopital')
    
    return render(request, 'admin/dashboard.html', {
        'total_donneurs': total_donneurs,
        'total_hopitaux': total_hopitaux,
        'hopitaux_non_valides': hopitaux_non_valides,
        'hopitaux_valides': hopitaux_valides,  
        'total_dons': total_dons,
        'demandes_actives': demandes_actives,
        'campagnes_a_venir': campagnes_a_venir,
        'hopitaux_attente': hopitaux_attente,
        'demandes_par_groupe': demandes_par_groupe,
        'demandes_par_ville': demandes_par_ville,  
    })

@login_required_dondesong
def valider_hopital(request, hopital_id):
    if not request.user.is_superuser:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('home')
    
    hopital = Hopital.objects.get(id=hopital_id)
    hopital.valide = True
    hopital.save()
    
    try:
        sujet = " DonDeSang - Votre compte hôpital a été validé !"
        message = f"""
Bonjour {hopital.nom},

Félicitations ! Votre compte hôpital sur DonDeSang a été validé par notre équipe administrative.

 Vous pouvez maintenant :
✓ Créer des demandes urgentes de sang
✓ Organiser des campagnes de donation
✓ Voir les réponses des donneurs
✓ Gérer votre profil et vos statistiques

 Connectez-vous dès maintenant : http://127.0.0.1:8000/connexion/

Nous vous remercions de votre engagement pour sauver des vies.

Cordialement,
L'équipe DonDeSang 
        """
        send_mail(sujet, message, settings.DEFAULT_FROM_EMAIL, [hopital.user.email], fail_silently=False)
        messages.success(request, f"Hôpital '{hopital.nom}' validé et email envoyé à {hopital.user.email}")
    except Exception as e:
        print(f" Erreur d'envoi d'email à {hopital.user.email}: {e}")
        messages.warning(request, f"Hôpital '{hopital.nom}' validé mais l'email n'a pas pu être envoyé.")
    
    return redirect('admin_dashboard')

@login_required_dondesong
def export_donneurs_csv(request):
    if not request.user.is_superuser:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('home')
    response = HttpResponse(content_type='text/csv')# Indique que la réponse est un fichier CSV
    response['Content-Disposition'] = 'attachment; filename="donneurs.csv"'
    writer = csv.writer(response)#
    writer.writerow(['Nom', 'Prénom', 'Email', 'Groupe sanguin', 'Ville', 'Téléphone', 'Date inscription'])
    for donneur in Donneur.objects.all():
        writer.writerow([
            donneur.user.last_name, donneur.user.first_name, donneur.user.email,
            donneur.groupe_sanguin, donneur.ville, donneur.telephone,
            donneur.user.date_joined.strftime('%Y-%m-%d')
        ])
    return response

@login_required_dondesong
def historique_dons(request):
    donneur = Donneur.objects.filter(user=request.user).first()
    if not donneur:
        return redirect('dashboard_donneur')
    dons = Don.objects.filter(donneur=donneur).order_by('-date_don')
    return render(request, 'donneur/historiquedonneur.html', {'dons': dons, 'donneur': donneur})