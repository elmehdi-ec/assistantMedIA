import streamlit as st
import pandas as pd
import os
from modules.resume import generer_resume

# 🔐 Charger le token Hugging Face depuis l'environnement
HF_TOKEN = os.getenv("HF_TOKEN")

# 📁 Charger les cas simulés
DATA_PATH = "data/cas_simules.csv"
try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
except Exception:
    st.error("❌ Impossible de charger les cas simulés.")
    st.stop()

# 👤 Sélection du médecin
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    medecin_id = st.selectbox("👩‍⚕️ Choisissez votre profil :", df["Médecin"].unique())
    mode_demo = st.checkbox("🧪 Mode démo", value=False)

st.title("🩺 Assistant IA Clinique")
st.markdown("Génération automatique des résumés médicaux via intelligence artificielle.")

# 📊 Affichage des cas cliniques
st.dataframe(df, use_container_width=True)

# ➕ Ajouter la colonne Résumé IA si absente
if "Résumé IA" not in df.columns:
    df["Résumé IA"] = ""

# 🧠 Générer les résumés IA
if st.button("🔄 Générer les résumés IA"):
    st.info("📡 Résumés en cours de génération...")
    for i, row in df.iterrows():
        symptomes = row.get("Symptômes", "")
        if isinstance(symptomes, str) and symptomes.strip():
            resume = generer_resume(symptomes, medecin_id, HF_TOKEN, mode_demo=mode_demo)
            df.at[i, "Résumé IA"] = resume
    st.success("✅ Résumés générés")

# 📥 Télécharger les données enrichies
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Télécharger les cas enrichis (.csv)",
    data=csv,
    file_name="cas_cliniques_enrichis.csv",
    mime="text/csv"
)
