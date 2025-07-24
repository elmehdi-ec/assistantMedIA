import streamlit as st
import pandas as pd
import yaml
from modules.resume import generer_resume

def charger_settings():
    try:
        with open("config/settings.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f).get("assistant", {})
    except Exception:
        return {}

settings = charger_settings()
DATA_PATH = "data/cas_simules.csv"

try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
except Exception:
    st.error("❌ Le fichier CSV est introuvable.")
    st.stop()

st.set_page_config(page_title=settings.get("nom_projet", "Assistant IA Médicale"), layout="wide")
st.title("🧠 " + settings.get("nom_projet", "Assistant IA Médicale"))
st.markdown(settings.get("message_accueil", "Bienvenue 👋"))

# 🔐 Récupération du token HF
hf_token = st.secrets.get("HF_TOKEN", None)
mode_demo = st.sidebar.checkbox("🧪 Mode démo (offline)", value=False)

if hf_token is None and not mode_demo:
    st.warning("⚠️ Aucun HF_TOKEN configuré. Activez le mode démo ou ajoutez le token dans .streamlit/secrets.toml.")

# 👨‍⚕️ Médecin référent
st.sidebar.markdown("## 🩺 Médecin référent")
if "Médecin" in df.columns:
    medecin_id = st.sidebar.selectbox("👨‍⚕️ Sélectionnez :", df["Médecin"].dropna().unique())
else:
    medecin_id = st.sidebar.text_input("👨‍⚕️ Nom du médecin :", "Dr Elmehdi")

# 🔄 Préparation de la colonne Résumé IA
if "Résumé IA" not in df.columns:
    df["Résumé IA"] = ""

st.subheader("📋 Cas cliniques")
st.dataframe(df, use_container_width=True)

# 🎯 Génération des résumés IA
if st.button("🔁 Générer les résumés IA"):
    st.info("🧠 Résumés en cours via BloomZ…")
    for i, row in df.iterrows():
        symptomes = row.get("Symptômes", "")
        if isinstance(symptomes, str) and symptomes.strip():
            try:
                resume = generer_resume(symptomes, medecin_id, hf_token=hf_token, mode_demo=mode_demo)
            except Exception as e:
                resume = f"❌ Erreur : {str(e)}"
            df.at[i, "Résumé IA"] = resume
    st.success("✅ Résumés générés.")

# 📥 Export CSV
if settings.get("export_csv", True):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Télécharger le CSV enrichi", data=csv, file_name="cas_cliniques_enrichis.csv", mime="text/csv")
