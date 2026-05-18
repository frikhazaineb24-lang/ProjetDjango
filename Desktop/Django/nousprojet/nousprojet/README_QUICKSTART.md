# 🚀 DonDeSong - Guide de démarrage rapide

## Installation & Setup

### 1. Prérequis
- Python 3.11+
- Django 4.2.28
- SQLite (inclus avec Python)

### 2. Cloner/Accéder au projet
```bash
cd c:\Users\User\Desktop\project_final\nousprojet
```

### 3. Environnement virtuel (optionnel mais recommandé)
```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Migrations Django
```bash
python manage.py migrate
```

### 5. Créer un administrateur
```bash
python manage.py createsuperuser
# Suivre les prompts pour créer un compte admin
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

Le site sera accessible à: **http://127.0.0.1:8000/**

## 🎯 Accès aux interfaces

### Page d'accueil
- URL: `http://127.0.0.1:8000/`
- Accès: Public (pas d'authentification requise)

### Inscription Donneur
- URL: `http://127.0.0.1:8000/inscription/donneur/`
- Créer un compte donneur avec groupe sanguin

### Inscription Hôpital
- URL: `http://127.0.0.1:8000/inscription/hopital/`
- Créer un compte hôpital (en attente de validation admin)

### Connexion
- URL: `http://127.0.0.1:8000/connexion/`
- Identifiant: username/email
- Mot de passe: password

### Dashboard Donneur
- URL: `http://127.0.0.1:8000/donneur/` (après authentification)
- Voir les demandes urgentes
- S'inscrire aux campagnes
- Enregistrer des dons
- Voir l'historique

### Dashboard Hôpital  
- URL: `http://127.0.0.1:8000/hopital/` (après authentification + validation)
- Créer des demandes urgentes
- Organiser des campagnes
- Voir les réponses des donneurs

### Admin Django
- URL: `http://127.0.0.1:8000/admin/`
- Identifiant: administrateur créé avec `createsuperuser`
- Gérer tous les modèles
- Valider les hôpitaux
- Exporter les données

## 📁 Structure du projet

```
nousprojet/
├── manage.py                  # Commande Django
├── db.sqlite3                 # Base de données
├── CORRECTIONS.md             # Documentation des corrections
├── README_QUICKSTART.md       # Ce fichier
│
├── nousprojet/                # Configuration Django
│   ├── settings.py            # Paramètres Django
│   ├── urls.py                # URLs principales
│   ├── wsgi.py                # WSGI pour production
│   └── asgi.py                # ASGI pour async
│
└── dondesong/                 # Application principale
    ├── models.py              # Modèles de données
    ├── views.py               # Vues/Logique métier
    ├── urls.py                # URLs de l'app
    ├── forms.py               # Formulaires Django
    ├── admin.py               # Configuration admin
    │
    ├── static/
    │   └── css/
    │       └── base.css       # Styles professionnel (NOUVEAU)
    │
    ├── templates/
    │   ├── dondesong/         # Templates de base
    │   ├── registration/      # Inscription & Connexion
    │   ├── donneur/           # Templates donneur
    │   ├── hopital/           # Templates hôpital
    │   ├── campagnes/         # Templates campagnes
    │   └── admin/             # Templates admin
    │
    └── migrations/            # Migrations BDD
```

## 🔑 Rôles & Permissions

### 1. Administrateur (Superuser)
- Accès: `/admin/`
- Permissions: Toutes
- Actions:
  - Valider/révoquer les hôpitaux
  - Gérer les donneurs
  - Voir les statistiques
  - Exporter les données

### 2. Donneur
- Accès: `/donneur/`
- Permissions: Profil donneur
- Actions:
  - Voir les demandes urgentes compatibles
  - S'inscrire aux campagnes
  - Enregistrer des dons
  - Consulter l'historique

### 3. Hôpital
- Accès: `/hopital/` (après validation)
- Permissions: Profil hôpital
- Actions:
  - Créer des demandes urgentes
  - Organiser des campagnes
  - Voir les réponses des donneurs
  - Statistiques

## 💡 Fonctionnalités principales

### 1. Gestion des dons
- Enregistrement du groupe sanguin
- Suivi de l'éligibilité (56j pour hommes, 84j pour femmes)
- Historique des dons

### 2. Demandes urgentes
- Création par les hôpitaux
- Appel aux donneurs compatibles
- Suivi des réponses

### 3. Campagnes de collecte
- Création avec créneaux horaires
- Gestion de la capacité
- Inscription des donneurs

### 4. Système de notifications
- Emails de bienvenue
- Notifications de validation
- Appels d'urgence

## 🎨 CSS & Styling

Le fichier CSS (`base.css`) inclut:
- **Navbar** - Navigation principale avec logo animé
- **Sidebar** - Navigation secondaire
- **Forms** - Formulaires professionnels
- **Buttons** - Boutons avec effets
- **Cards** - Conteneurs avec shadows
- **Tables** - Tableaux de données stylisés
- **Alerts** - Notifications avec couleurs d'importance
- **Responsive** - Design mobile-friendly

### Couleurs principales
- Primaire: `#e74c3c` (Rouge - Sang)
- Secondaire: `#2c3e50` (Gris foncé)
- Succès: `#27ae60` (Vert)
- Danger: `#e74c3c` (Rouge)
- Warning: `#f39c12` (Orange)
- Info: `#3498db` (Bleu)

## 🧪 Tests & Débogage

### Vérifier la configuration
```bash
python manage.py check
```

### Voir les erreurs de migration
```bash
python manage.py showmigrations
```

### Créer des données de test
```bash
python manage.py shell
```

Ensuite dans le shell:
```python
from django.contrib.auth.models import User
from dondesong.models import Donneur

# Créer un utilisateur
user = User.objects.create_user('test_donor', 'test@example.com', 'password123')

# Créer un donneur
Donneur.objects.create(
    user=user,
    groupe_sanguin='O+',
    sexe='H',
    date_naissance='1990-01-01',
    ville='Paris',
    telephone='0612345678'
)
```

## 📊 Configuration avancée

### Variables d'environnement
Pour la production, créer un `.env`:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://...
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
```

### Email (Production)
Configurer dans `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## 🐛 Dépannage courant

### Port 8000 déjà utilisé
```bash
python manage.py runserver 8001
```

### Migrations non appliquées
```bash
python manage.py migrate --fake-initial
```

### Fichiers statiques non chargés
```bash
python manage.py collectstatic --noinput
```

### Erreur de base de données
```bash
rm db.sqlite3
python manage.py migrate
```

## 📞 Support

Pour toute question ou problème:
1. Vérifier les logs dans la console
2. Utiliser `python manage.py check`
3. Consulter la documentation Django
4. Vérifier les URLs dans `urls.py`

---

**Bon développement! 🩸**
