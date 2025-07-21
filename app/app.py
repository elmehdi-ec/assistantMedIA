import streamlit as st
import pandas as pd
import os
from app.modules.resume import generer_resume

# 📁 Charger les cas simulés
DATA_PATH = "data/cas_simules.csv"
try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
except Exception:
    st.error("❌ Impossible de charger les cas simulés")
    st.stop()

# 👤 Sélection du médecin
with st.sidebar:
    medecin_id = st.selectbox("👤 Sélectionnez votre profil", options=["Dr_Elmehdi", "Dr_Salma", "Dr_Imane"])
    mode_demo = st.checkbox("🧪 Activer le mode démo", value=False)

st.title("🩺 Assistant IA Clinique — Résumé intelligent des cas")

# 📋 Affichage du tableau
st.dataframe(df, use_container_width=True)

# 🧠 Ajouter une colonne Résumé IA
if "Résumé IA" not in df.columns:
    df["Résumé IA"] = ""

# 🔄 Générer les résumés
if st.button("🔄 Générer les résumés IA"):
    st.info("Génération en cours...")
    for i, row in df.iterrows():
        symptomes = row.get("Symptômes", "")
        if isinstance(symptomes, str) and symptomes.strip():
            resume = generer_resume(symptomes, medecin_id, mode_demo=mode_demo)
            df.at[i, "Résumé IA"] = resume
    st.success("✅ Résumés générés")

# 📤 Export possible ?
if st.download_button