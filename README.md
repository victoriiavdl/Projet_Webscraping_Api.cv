# ReviewBot - Réponse automatique aux avis clients

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://reviewbot.streamlit.app)

> **Accéder à l'application :** [https://reviewbot.streamlit.app](https://reviewbot.streamlit.app)

## Présentation

**ReviewBot** est un outil de web scraping et de NLP qui collecte automatiquement les avis clients sur les principales plateformes en ligne, puis génère des réponses personnalisées adaptées au ton et au sentiment de chaque avis.

L'application permet de :
- **Extraire** les avis et notes depuis 5 plateformes (Trustpilot, Yelp, Google Play Store, Amazon, Google Maps)
- **Analyser** automatiquement le sentiment et la langue de chaque avis
- **Générer** des réponses personnalisées grâce à un modèle de langage (GPT4All) ou des templates multilingues
- **Exporter** les résultats en CSV pour une exploitation ultérieure

## Plateformes supportées

| Plateforme | Type d'avis | Méthode |
|------------|-------------|---------|
| **Trustpilot** | Avis entreprises | Recherche par nom + pagination |
| **Yelp** | Avis commerces locaux | Recherche par nom + pagination |
| **Google Play Store** | Avis applications | Recherche par nom + scroll infini |
| **Amazon** | Avis produits | Recherche par mot-clé + pagination (cookies requis) |
| **Google Maps** | Avis lieux / établissements | Extraction par URL + scroll infini |

## Structure du projet

```
projet_webscraping_api/
├── app.py                                      # Interface Streamlit
├── scraping.ipynb                              # Notebook d'exploration
├── functions/
│   ├── API/
│   │   └── main.py                             # API FastAPI (endpoints REST)
│   ├── generator/
│   │   └── response_generator.py               # Génération de réponses (NLP)
│   └── scrapping/
│       ├── functions_trustpilot.py              # Scraping Trustpilot
│       ├── functions_yelp.py                    # Scraping Yelp
│       ├── functions_play_store.py              # Scraping Google Play Store
│       ├── functions_amazon.py                  # Scraping Amazon
│       └── functions_google_reviews.py          # Scraping Google Maps
├── pyproject.toml                              # Configuration & dépendances
└── .gitignore
```

## Stack technique

- **Python 3.12+**
- **Streamlit** — interface web interactive
- **Selenium** — web scraping dynamique (navigation, scroll, pagination)
- **FastAPI** — API REST pour intégration externe
- **Transformers (HuggingFace)** — analyse de sentiment (`nlptown/bert-base-multilingual-uncased-sentiment`)
- **GPT4All** — génération de réponses en local (modèle `orca-mini-3b`)
- **langdetect** — détection automatique de la langue
- **Pandas** — manipulation des données

## Installation locale

```bash
git clone https://github.com/victoriiavdl/projet_webscraping_api.cv.git
cd projet_webscraping_api.cv

# Avec poetry (recommandé)
poetry install
streamlit run app.py

# Ou lancer l'API FastAPI
uvicorn functions.API.main:app
```

## Contexte

Ce projet a été réalisé dans le cadre d'un cours de **Web Scraping & API** (Master MOSEF, Sorbonne). L'objectif était de concevoir un système complet de collecte d'avis clients par web scraping, couplé à un module de génération automatique de réponses par NLP.
