# Projet_Webscraping_Api

## Auteurs :
- FOGUE FEUSSI Franck Jorel
- VIDAL Victoria
- AIT SAID Melina 

## Objectif du projet
Le but du projet est de concevoir un système capable de générer automatiquement des
propositions de réponses personnalisées aux avis clients collectés sur différentes plateformes en ligne.

## Plateformes supportées
- **Trustpilot** — Avis entreprises
- **Yelp** — Avis commerces locaux
- **Google Play Store** — Avis applications
- **Amazon** — Avis produits
- **Google Maps** — Avis lieux / établissements

## Installation du projet
1. **Prérequis**
- Python >= 3.12
- Git Bash (ou terminal équivalent)
- Google Chrome (pour Selenium)

2. **Cloner le projet**
```bash
git clone https://github.com/victoriiavdl/projet_webscraping_api.cv.git
cd projet_webscraping_api.cv
```

3. **Créer un environnement virtuel**
```bash
pip install virtualenv
virtualenv .venv
```

Activer l'environnement :
```bash
# Windows
source .venv/Scripts/activate

# Linux / MacOS
source .venv/bin/activate
```

4. **Installer les dépendances**
```bash
poetry install
```

## Utilisation

### Interface Streamlit (recommandé pour tester)
```bash
streamlit run app.py
```
Ouvrez ensuite votre navigateur sur l'URL affichée (par défaut `http://localhost:8501`).

L'interface permet de :
- Choisir une plateforme source
- Rechercher une entreprise / un produit
- Extraire les avis en temps réel
- Générer des réponses automatiques
- Exporter les résultats en CSV

### API FastAPI
```bash
uvicorn functions.API.main:app
```
Documentation interactive : `http://127.0.0.1:8000/docs`

### Note pour Amazon
Le scraping Amazon nécessite une connexion manuelle préalable via `save_cookies()` dans le notebook `scraping.ipynb`. Cette étape ne doit être réalisée qu'une seule fois.
