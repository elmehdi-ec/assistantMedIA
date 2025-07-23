import streamlit as st
import pandas as pd
import os
import yaml
from modules.resume import generer_resume

# 🔐 Chargement du token HF
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
    st.error("❌ Fichier 'cas_simules.csv' introuvable.")
    st.stop()

# 🎨 Interface Streamlit
st.set_page_config(page_title=settings.get("nom_projet", "Assistant IA"), layout="wide")
st.title("🧠 " + settings.get("nom_projet", "Assistant IA Clinique"))

if settings.get("affichage_version_ui", True):
    mode_label = "Démo" if settings.get("mode_fallback") == "demo" else "IA"
    st.caption(f"🧬 Version : {settings.get('version', '1.0')} — Mode : {mode_label}")

st.markdown(settings.get("message_accueil", "Bienvenue 👋"))

# 🩺 Profil médecin
st.sidebar.markdown("## 🩺 Profil médecin")
if "Médecin" in df.columns:
    medecin_id = st.sidebar.selectbox("👨‍⚕️ Sélectionnez votre profil :", df["Médecin"].dropna().unique())
else:
    default_col = df.columns[0] if len(df.columns) > 0 else "Médecin"
    st.sidebar.warning(f"⚠️ Colonne 'Médecin' absente — utilisation de '{default_col}'")
    medecin_id = st.sidebar.selectbox("👨‍⚕️ Profil :", df[default_col].dropna().unique())

# 🧪 Mode démo activable
mode_demo = st.sidebar.checkbox("🧪 Activer le mode démo (offline)", value=(settings.get("mode_fallback") == "demo"))

# ➕ Ajout colonne Résumé IA si absente
if "Résumé IA" not in df.columns:
    df["Résumé IA"] = ""

# 📋 Affichage des cas cliniques
st.subheader("📋 Cas cliniques")
st.dataframe(df, use_container_width=True)

# 🔁 Génération des résumés IA
if st.button("🔁 Générer les résumés IA"):
    st.info("📡 Envoi des cas au modèle IA...")

    for i, row in df.iterrows():
        symptomes = row.get("Symptômes", "")
        if isinstance(symptomes, str) and symptomes.strip():
            resume = generer_resume(symptomes, medecin_id, HF_TOKEN, mode_demo=mode_demo)
            df.at[i, "Résumé IA"] = resume

    st.success("✅ Résumés IA générés.")

# 📥 Export CSV
if settings.get("export_csv", True):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger les cas enrichis (.csv)",
        data=csv,
        file_name="cas_cliniques_enrichis.csv",
        mime="text/csv"
    )
