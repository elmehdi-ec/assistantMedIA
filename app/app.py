import streamlit as st
import pandas as pd
import os
import yaml
from modules.resume import generer_resume

# 🔐 Chargement du token Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")

# ⚙️ Chargement des paramètres globaux
def charger_settings():
    try:
        with open("config/settings.yaml", "r", encoding="utf-8") as file:
            return yaml.safe_load(file).get("assistant", {})
    except Exception:
        return {}

settings = charger_settings()

# 📁 Chargement des cas cliniques
DATA_PATH = "data/cas_simules.csv"
try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
except Exception:
    st.error("❌ Fichier 'cas_simules.csv' introuvable ou illisible.")
    st.stop()

# 🎨 Interface Streamlit — configuration initiale
st.set_page_config(
    page_title=settings.get("nom_projet", "Assistant IA"),
    layout="wide"
)

st.title("🧠 " + settings.get("nom_projet", "Assistant IA Clinique"))

if settings.get("affichage_version_ui", True):
    mode_label = "Démo" if settings.get("mode_fallback") == "demo" else "IA"
    st.caption(f"🧬 Version : {settings.get('version', '1.0')} — Mode : {mode_label}")

st.markdown(settings.get("message_accueil", "Bienvenue 👋"))

# 🧑‍⚕️ Sélection du profil médecin
st.sidebar.markdown("## 🧑‍⚕️ Profil médecin")
if "Médecin" in df.columns:
    medecin_id = st.sidebar.selectbox("Sélectionnez votre profil :", df["Médecin"].dropna().unique())
else:
    default_col = df.columns[0] if len(df.columns) > 0 else "Médecin"
    st.sidebar.warning(f"⚠️ Colonne 'Médecin' absente — utilisation de '{default_col}'")
    medecin_id = st.sidebar.selectbox("Profil :", df[default_col].dropna().unique())

# ⚙️ Mode démo activable
mode_demo = st.sidebar.checkbox("🧪 Mode démo (offline)", value=(settings.get("mode_fallback") == "demo"))

# 🩺 Résumé IA — ajouter la colonne si absente
if "Résumé IA" not in df.columns:
    df["Résumé IA"] = ""

# 📋 Affichage des cas cliniques
st.subheader("📋 Cas cliniques")
st.dataframe(df, use_container_width=True)

# 🔁 Génération des résumés IA
if st.button("🔁 Générer les résumés IA"):
    st.info("📡 Envoi des cas au moteur IA...")

    for i, row in df.iterrows():
        symptomes = row.get("Symptômes", "")
        if isinstance
