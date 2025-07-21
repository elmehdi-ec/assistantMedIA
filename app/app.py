import streamlit as st
import pandas as pd
import os
from modules.resume import generer_resume

HF_TOKEN = os.getenv("HF_TOKEN")  # 🔐 Chargement sécurisé du token Hugging Face

# 📁 Chargement des cas cliniques
DATA_PATH = "data/cas_simules.csv"
try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
except Exception:
    st.error("❌ Fichier 'cas_simules.csv' introuvable ou illisible.")
    st.stop()

st.title("🩺 Assistant IA Clinique — Résumés Médicaux")
st.markdown("Outil intelligent de synthèse médicale multilingue pour soutenir le triage et la prise de décision.")

# 📌 Affichage des colonnes pour debug rapide
st.sidebar.markdown("## 🔍 Colonnes détectées")
st.sidebar.write(list(df.columns))

# 👤 Détection ou adaptation de la colonne 'Médecin'
if "Médecin" in df.columns:
    medecin_id = st.sidebar.selectbox("👩‍⚕️ Choisissez votre profil :", df["Médecin"].dropna().unique())
else:
    # ✅ Fallback si colonne absente
    default_column = df.columns[0] if len(df.columns) > 0 else "Médecin"
    st.warning(f"⚠️ Colonne 'Médecin' absente — utilisation de '{default_column}' par défaut.")
    medecin_id = st.sidebar.selectbox("👩‍⚕️ Choisissez votre profil :", df[default_column].dropna().unique())

# 🧪 Mode démo activable
mode_demo = st.sidebar.checkbox("🧪 Activer le mode démo (offline)", value=False)

# ➕ Ajout de la colonne Résumé IA si absente
if "Résumé IA" not in df.columns:
    df["Résumé IA"] = ""

# 📊 Affichage tableau interactif
st.subheader("📋 Cas cliniques détectés")
st.dataframe(df, use_container_width=True)

# 🔄 Génération des résumés IA
if st.button("🔁 Générer les résumés IA"):
    st.info("🧠 Résumés en cours de création...")
    for i, row in df.iterrows():
        symptomes = row.get("Symptômes", "")
        if isinstance(symptomes, str) and symptomes.strip():
            resume = generer_resume(symptomes, medecin_id, HF_TOKEN, mode_demo=mode_demo)
            df.at[i, "Résumé IA"] = resume
    st.success("✅ Résumés IA ajoutés avec succès.")

# 📥 Export CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📁 Télécharger les cas enrichis (.csv)",
    data=csv,
    file_name="cas_cliniques_enrichis.csv",
    mime="text/csv"
)
