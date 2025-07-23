import os
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Assistant IA Médical", layout="wide")

st.title("🧠 Assistant IA Médical")
st.markdown("Version : **1.0.0** — Mode : **IA**")

# === TOKEN ===
HF_TOKEN = os.getenv("HF_TOKEN")
DEMO_MODE = HF_TOKEN is None

# Affichage de l’état du token
if DEMO_MODE:
    st.warning("🔐 Mode démo activé — aucun token Hugging Face détecté.")
else:
    st.success(f"🔐 Token Hugging Face détecté. Début : `{HF_TOKEN[:4]}...`")

# === Données ===
data = pd.DataFrame([
    {"Nom": "Ahmed", "Âge": 65, "Sexe": "Homme", "Symptômes": "Fièvre, toux, essoufflement", "Gravité": 8},
    {"Nom": "Salma", "Âge": 32, "Sexe": "Femme", "Symptômes": "Céphalée, douleur oreille", "Gravité": 3},
    {"Nom": "Youssef", "Âge": 74, "Sexe": "Homme", "Symptômes": "Confusion, chute récente", "Gravité": 9},
    {"Nom": "Imane", "Âge": 19, "Sexe": "Femme", "Symptômes": "Maux gorge, fièvre", "Gravité": 4},
])

st.subheader("📋 Cas cliniques")
st.dataframe(data, use_container_width=True)

# === Résumés IA ===
def generate_summary(row):
    prompt = f"Patient de {row['Âge']} ans, {row['Sexe']}, présente les symptômes suivants : {row['Symptômes']}. Génère un résumé clinique."
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-base",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except Exception as e:
        st.error(f"❌ Erreur IA : {e}")
        return "Erreur IA"

if st.button("🧠 Générer les résumés IA"):
    if DEMO_MODE:
        st.warning("Le mode démo est activé. Définissez HF_TOKEN pour activer l’IA.")
    else:
        st.info("Envoi des cas au moteur IA...")
        data["Résumé IA"] = data.apply(generate_summary, axis=1)
        st.success("✅ Résumés générés !")
        st.dataframe(data, use_container_width=True)

# === Export CSV ===
st.download_button(
    label="📥 Télécharger les cas enrichis (.csv)",
    data=data.to_csv(index=False).encode("utf-8"),
    file_name="cas_cliniques_avec_resumes.csv",
    mime="text/csv",
)
