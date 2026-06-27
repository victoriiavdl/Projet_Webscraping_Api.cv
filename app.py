import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="Web Scraping - Avis Clients",
    page_icon="🔍",
    layout="wide",
)

st.title("Web Scraping & Réponse Automatique aux Avis Clients")
st.markdown(
    "Cette application permet d'extraire des avis clients depuis plusieurs plateformes "
    "et de générer automatiquement des réponses personnalisées grâce au NLP."
)

st.divider()

# --- Sidebar ---
st.sidebar.header("Configuration du scraping")

source = st.sidebar.selectbox(
    "Plateforme source",
    ["Trustpilot", "Yelp", "Google Play Store", "Amazon", "Google Maps"],
)

search_query = st.sidebar.text_input(
    "Recherche (nom d'entreprise / produit)",
    placeholder="ex: Burger King, Boursorama, Netflix...",
)

if source == "Amazon":
    st.sidebar.warning(
        "Le scraping Amazon n'est pas disponible en démo : "
        "il nécessite une authentification par cookies (connexion manuelle préalable)."
    )

max_reviews = st.sidebar.slider("Nombre max d'avis", 1, 50, 5)

generate_responses = st.sidebar.checkbox("Générer les réponses automatiques", value=False)

run_button = st.sidebar.button("Lancer le scraping", type="primary", use_container_width=True)

# --- Mapping ---
SOURCE_MAP = {
    "Trustpilot": "trustpilot",
    "Yelp": "yelp",
    "Google Play Store": "playstore",
    "Amazon": "amazon",
    "Google Maps": "google",
}


def run_scraping(source_key: str, query: str, max_rev: int):
    if source_key == "trustpilot":
        from functions.scrapping.functions_trustpilot import extract_reviews_and_ratings_from_trustpilot
        return extract_reviews_and_ratings_from_trustpilot(query, max_rev)
    elif source_key == "yelp":
        from functions.scrapping.functions_yelp import extract_reviews_and_ratings_from_yelp
        return extract_reviews_and_ratings_from_yelp(query, max_rev)
    elif source_key == "playstore":
        from functions.scrapping.functions_play_store import extract_reviews_and_ratings_from_google_play_store
        return extract_reviews_and_ratings_from_google_play_store(query, max_rev)
    elif source_key == "amazon":
        from functions.scrapping.functions_amazon import extract_reviews_and_ratings_from_amazon
        return extract_reviews_and_ratings_from_amazon(query, max_rev)
    elif source_key == "google":
        from functions.scrapping.functions_google_reviews import extract_reviews_and_ratings_from_google_map
        return extract_reviews_and_ratings_from_google_map(query, max_rev)
    return []


def get_response_generator():
    if "generator" not in st.session_state:
        from functions.generator.response_generator import ResponseGenerator
        st.session_state.generator = ResponseGenerator(use_ai=False)
    return st.session_state.generator


# --- Main area ---
if run_button:
    if not search_query.strip():
        st.warning("Veuillez entrer un terme de recherche.")
    else:
        source_key = SOURCE_MAP[source]

        if source_key == "amazon":
            st.warning(
                "Le scraping Amazon nécessite une connexion manuelle préalable "
                "(cookies). Assurez-vous d'avoir exécuté `save_cookies()` au moins une fois."
            )

        with st.spinner(f"Extraction des avis depuis {source}..."):
            start = time.time()
            try:
                reviews = run_scraping(source_key, search_query, max_reviews)
                elapsed = time.time() - start
            except Exception as e:
                st.error(f"Erreur lors du scraping : {e}")
                reviews = []
                elapsed = 0

        if reviews:
            st.success(f"{len(reviews)} avis extraits en {elapsed:.1f}s")

            if generate_responses:
                generator = get_response_generator()
                with st.spinner("Génération des réponses..."):
                    for review in reviews:
                        review_text = review.get("review", "")
                        rating = review.get("rating")
                        if review_text:
                            review["sentiment"] = generator.detect_sentiment(review_text)
                            review["langue"] = generator.detect_language(review_text)
                            review["reponse_generee"] = generator.generate_response(
                                review_text=review_text, rating=rating
                            )

            df = pd.DataFrame(reviews)

            # --- Stats ---
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avis extraits", len(reviews))
            with col2:
                if "rating" in df.columns:
                    st.metric("Note moyenne", f"{df['rating'].mean():.1f} / 5")
            with col3:
                st.metric("Temps d'extraction", f"{elapsed:.1f}s")

            st.divider()

            # --- Tabs ---
            tab_table, tab_detail = st.tabs(["Tableau", "Détail par avis"])

            with tab_table:
                st.dataframe(df, use_container_width=True, hide_index=True)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Télécharger en CSV",
                    csv,
                    file_name=f"avis_{source_key}_{search_query}.csv",
                    mime="text/csv",
                )

            with tab_detail:
                for i, review in enumerate(reviews):
                    rating = review.get("rating", "?")
                    stars = "⭐" * int(rating) if isinstance(rating, (int, float)) else ""
                    with st.expander(f"Avis #{i+1} — {stars} ({rating}/5)"):
                        st.write(review.get("review", ""))
                        if "reponse_generee" in review:
                            st.divider()
                            st.markdown("**Réponse générée :**")
                            st.info(review["reponse_generee"])
                            if "sentiment" in review:
                                st.caption(
                                    f"Sentiment : {review['sentiment']} | "
                                    f"Langue : {review['langue']}"
                                )
        elif elapsed > 0:
            st.warning("Aucun avis trouvé pour cette recherche.")

else:
    # --- Page d'accueil ---
    st.info("Configurez les paramètres dans la barre latérale puis cliquez sur **Lancer le scraping**.")

    st.markdown("### Plateformes supportées")
    cols = st.columns(5)
    platforms = [
        ("Trustpilot", "Avis entreprises"),
        ("Yelp", "Avis commerces locaux"),
        ("Google Play Store", "Avis applications"),
        ("Amazon", "Avis produits"),
        ("Google Maps", "Avis lieux / établissements"),
    ]
    for col, (name, desc) in zip(cols, platforms):
        with col:
            st.markdown(f"**{name}**")
            st.caption(desc)

    st.markdown("### Fonctionnalités")
    st.markdown(
        "- Extraction automatique des avis et notes\n"
        "- Détection de la langue et du sentiment\n"
        "- Génération automatique de réponses personnalisées\n"
        "- Export CSV des résultats\n"
        "- API FastAPI disponible (`uvicorn functions.API.main:app`)"
    )
