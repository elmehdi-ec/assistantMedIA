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
    st.error("❌ CSV introuvable ou illisible.")
    st.stop()

st.set_page_config(page_title=settings.get("nom_projet", "Assistant IA Médicale"), layout="wide")
st.title("🧠 " + settings.get("nom_projet", "Assistant IA Médicale"))
st.markdown(settings.get("message_accueil", "Bienvenue 👋"))

mode_demo = st.sidebar.checkbox("🧪 Mode démo (offline)", value=False)
mode_label = "Démo" if mode_demo else "IA BloomZ"
st.caption(f"🧬 Mode : {mode_label}")

hf_token = st.secrets.get("HF_TOKEN", None)
if hf_token is None and not mode_demo:
    st.warning("⚠️ Aucun HF_TOKEN configuré. Activez le mode démo ou ajoutez votre token.")

st.sidebar.markdown("## 🩺 Médecin référent")
if "Médecin" in df.columns:
    medecin_id = st.sidebar.selectbox("👨‍⚕️ Sélectionnez :", df["Médecin"].dropna().unique())
else:
    medecin_id = st.sidebar.text_input("👨‍⚕️ Nom du médecin :", "Dr Elmehdi")

if "Résumé IA" not in df.columns:
    df["Résumé IA"] = ""

st.subheader("📋 Cas cliniques")
st.dataframe(df, use_container_width=True)

if st.button("🔁 Générer les résumés IA"):
    st.info("🧠 Génération via BloomZ en cours…")
    for i, row in df.iterrows():
        symptomes = row.get("Symptômes", "")
        if isinstance(symptomes, str) and symptomes.strip():
            try:
                resume = generer_resume(symptomes, medecin_id, hf_token=hf_token, mode_demo=mode_demo)
            except Exception as e:
                resume = f"❌ Erreur : {str(e)}"
            df.at[i, "Résumé IA"] = resume
    st.success("✅ Résumés générés.")

if settings.get("export_csv", True):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Télécharger le CSV enrichi", data=csv, file_name="cas_cliniques_enrichis.csv", mime="text/csv")
