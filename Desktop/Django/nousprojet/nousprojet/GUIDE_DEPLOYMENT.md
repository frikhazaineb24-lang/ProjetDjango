# 🚀 Guide de Déploiement - DonDeSang

## Plateforme recommandée : **Railway.app**

Railway est la meilleure option pour déployer Django rapidement. C'est gratuit (avec crédit gratuit) et très simple.

---

## ✅ Prérequis

- ✅ Compte GitHub (créer un compte gratuit sur https://github.com)
- ✅ Compte Railway (créer sur https://railway.app)
- ✅ Git installé (https://git-scm.com)

---

## 📝 Étapes de déploiement

### **Étape 1 : Initialiser Git et pousser vers GitHub**

```bash
# Aller dans le dossier du projet
cd c:\Users\User\Desktop\Django\nousprojet\nousprojet

# Initialiser un repo Git (si pas déjà fait)
git init

# Ajouter tous les fichiers
git add .

# Commit initial
git commit -m "Préparation pour déploiement"

# Ajouter une remote GitHub
git remote add origin https://github.com/frikhazaineb24-lang/dondesong.git

# Pousser vers GitHub
git branch -M main
git push -u origin main
```

---

### **Étape 2 : Créer un compte Railway et déployer**

1. **Accéder à Railway.app**
   - Aller sur https://railway.app
   - Cliquer sur "Sign Up" (s'inscrire)
   - Utiliser GitHub pour se connecter (c'est plus facile)

2. **Créer un nouveau projet**
   - Cliquer sur "New Project"
   - Sélectionner "Deploy from GitHub repo"
   - Sélectionner ton repo `dondesong`
   - Cliquer sur "Deploy"

3. **Configurer les variables d'environnement**
   - Aller dans l'onglet "Variables" du projet
   - Ajouter ces variables :

   ```
   DJANGO_SETTINGS_MODULE=nousprojet.settings
   SECRET_KEY=ta-clé-secrète-complexe
   DEBUG=False
   ALLOWED_HOSTS=*
   ```

4. **Attendre la déploiement**
   - Railway va automatiquement :
     - Installer les dépendances (pip install -r requirements.txt)
     - Exécuter les migrations
     - Démarrer le serveur
   - Tu recevras une URL du type : `https://dondesong-production.up.railway.app`

---

## 🔐 Sécurité - Points importants

### **1. Générer une nouvelle SECRET_KEY**

```bash
# Dans un terminal Python :
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie cette clé et ajoute-la dans les variables d'environnement Railway.

### **2. Créer un super-utilisateur sur le serveur déployé**

Après le déploiement, tu peux accéder au shell Django via Railway :

```bash
# Dans le terminal Railway
python manage.py createsuperuser
```

---

## 🎯 Autres plateformes de déploiement

Si tu veux explorer d'autres options :

### **PythonAnywhere (Plus facile, moins flexible)**
- Site : https://www.pythonanywhere.com/
- Avantage : Très simple, gratuit avec limitations
- Inconvénient : Moins flexible, interface plus complexe

### **Render (Très similaire à Railway)**
- Site : https://render.com/
- Avantage : Gratuit, facile, interface moderne
- Inconvénient : Légèrement plus lent que Railway

### **Heroku (Plus puissant, payant)**
- Site : https://www.heroku.com/
- Avantage : Très populaire, beaucoup de docs
- Inconvénient : Pas gratuit après l'arrêt des dynos gratuits

---

## 📱 Après le déploiement

### **Accéder à ton site**
- Va sur l'URL fournie par Railway
- Accès admin : `https://ton-url.railway.app/admin`
- Connecte-toi avec tes identifiants super-utilisateur

### **Mise à jour du site**
```bash
# Modifier le code localement
# Commit et push vers GitHub
git add .
git commit -m "Nouvelle fonctionnalité"
git push origin main

# Railway va redéployer automatiquement
```

### **Vérifier les logs**
- Dans Railway, onglet "Deployments"
- Cliquer sur un déploiement pour voir les logs

---

## ❌ Dépannage courant

### **Erreur 500 au déploiement**
- Vérifier les logs Railway
- Vérifier les variables d'environnement
- Assurer que migrations s'exécutent correctement

### **Les fichiers statiques ne chargent pas**
- Vérifier que WhiteNoise est dans le middleware
- Exécuter : `python manage.py collectstatic`

### **La base de données n'est pas persistée**
- Railway utilise par défaut une DB temporaire
- À migrer vers PostgreSQL (gratuit sur Railway)

---

## 🎉 Résumé

| Étape | Action |
|-------|--------|
| 1 | Initialiser Git et pousser code vers GitHub |
| 2 | Créer compte Railway |
| 3 | Connecter GitHub à Railway |
| 4 | Configurer variables d'environnement |
| 5 | Déployer et attendre |
| 6 | Créer super-utilisateur |
| 7 | Accéder à ton site en ligne |

---

**Questions ?** Consulte la doc Railway : https://docs.railway.app/

