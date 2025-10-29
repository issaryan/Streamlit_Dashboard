# 📊 Tableau de Bord d'Analyse de Données

Dashboard interactif pour transformer vos notebooks Jupyter en analyses professionnelles.

## 🚀 Déploiement sur Streamlit Community Cloud

### Prérequis
- Un compte GitHub (gratuit)
- Un compte Streamlit Community Cloud (gratuit)

### Étape 1 : Préparer votre projet

Votre structure de fichiers doit ressembler à :

```
votre-projet/
│
├── app.py                 # Application principale
├── requirements.txt       # Dépendances Python
├── README.md             # Ce fichier
├── .gitignore            # Fichiers à ignorer
│
└── examples/             # Exemples (optionnel)
    ├── loan_analyzer.ipynb
    └── loan_data.csv
```

### Étape 2 : Créer un dépôt GitHub

1. **Allez sur [github.com](https://github.com)**
2. **Cliquez sur "New repository"**
3. **Remplissez les informations :**
   - Repository name : `streamlit-dashboard-analyse`
   - Description : "Dashboard interactif pour analyse de notebooks Jupyter"
   - Visibilité : **Public** (requis pour le plan gratuit)
4. **Cliquez "Create repository"**

### Étape 3 : Uploader vos fichiers

**Option A : Via l'interface web GitHub**
- Cliquez sur "Add file" > "Upload files"
- Glissez-déposez : `app.py`, `requirements.txt`, `README.md`, `.gitignore`
- Commit : "Initial commit"

**Option B : Via Git en ligne de commande**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/votre-username/streamlit-dashboard-analyse.git
git push -u origin main
```

### Étape 4 : Déployer sur Streamlit Cloud

1. **Allez sur [share.streamlit.io](https://share.streamlit.io)**
2. **Connectez-vous avec votre compte GitHub**
3. **Cliquez sur "New app"**
4. **Configurez :**
   - Repository : `votre-username/streamlit-dashboard-analyse`
   - Branch : `main`
   - Main file path : `app.py`
   - App URL (optionnel) : `votre-nom-unique`
5. **Cliquez "Deploy!"**

⏱️ **Le déploiement prend 2-5 minutes**

### Étape 5 : Votre dashboard est en ligne ! 🎉

Votre URL sera : `https://votre-nom-unique.streamlit.app`

## 🔧 Configuration avancée (optionnel)

### Fichier .streamlit/config.toml

Créez un dossier `.streamlit/` avec un fichier `config.toml` :

```toml
[theme]
primaryColor = "#818CF8"
backgroundColor = "#0f1419"
secondaryBackgroundColor = "#1f2937"
textColor = "#FFFFFF"

[server]
maxUploadSize = 200
enableXsrfProtection = true
enableCORS = false

[browser]
gatherUsageStats = false
```

### Fichier .streamlit/secrets.toml (pour les secrets)

Si vous avez des clés API :

```toml
# Ne jamais commiter ce fichier !
api_key = "votre_clé_secrète"
```

Ajoutez les secrets via l'interface Streamlit Cloud :
- Paramètres de l'app > Secrets

## 📦 Mise à jour de l'application

1. **Modifiez vos fichiers localement**
2. **Commitez et poussez sur GitHub :**
   ```bash
   git add .
   git commit -m "Description des changements"
   git push
   ```
3. **Le dashboard se redéploie automatiquement !**

## 🛠️ Dépannage

### Erreur : "ModuleNotFoundError"
- Vérifiez que le module est dans `requirements.txt`
- Redéployez l'application

### L'app est lente
- Vérifiez la taille des fichiers uploadés
- Optimisez le code (mise en cache avec `@st.cache_data`)

### Erreur de mémoire
- Le plan gratuit a 1GB de RAM
- Réduisez la taille des données ou notebooks

## 📚 Ressources

- [Documentation Streamlit](https://docs.streamlit.io/)
- [Guide de déploiement](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Forum Streamlit](https://discuss.streamlit.io/)

## 📝 Utilisation

1. **Chargez vos fichiers** dans la sidebar
2. **Ajustez les paramètres** avec les sliders
3. **Lancez l'analyse** avec le bouton
4. **Explorez les résultats** dans la zone principale

## 🤝 Contribution

Pour contribuer à ce projet :
1. Forkez le repository
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Commitez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

MIT License - Libre d'utilisation

## 👨‍💻 Auteur

Koagne Issa Ryan - [GitHub](https://github.com/issaryan)

---

**✨ Bon déploiement !**