import streamlit as st
import pandas as pd
import yaml
from modules.resume import generer_resume

# 🔐 Lecture du token Hugging Face via Secrets
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except KeyError:
    HF_TOKEN = None

# 🔍 Vérification visuelle dans la sidebar
if HF_TOKEN and HF_TOKEN.strip() != "":
    st.sidebar.success("🔐 HF_TOKEN détecté ✔️")
else:
    st.sidebar.error("❌ HF_TOKEN manquant. Configurez-le dans Streamlit Cloud → Secrets.")
    st.stop()

# ⚙️ Chargement des paramètres personnalisés
def charger_settings():
    try:
        with open("config/settings.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f).get("assistant", {})
    except Exception:
        return {}

settings = charger_settings()

# 📁 Chargement des cas cliniques
DATA_PATH = "data/cas_simules.csv"
try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
except Exception:
    st.error("❌ Fichier 'cas_simules.csv' introuvable ou corrompu.")
    st.stop()

# 🎨 Configuration de l’interface
st.set_page_config(page_title=settings.get("nom_projet", "Assistant Médical IA"), layout="wide")
st.title("🧠 " + settings.get("nom_projet", "Assistant Médical IA"))
st.markdown(settings.get("message_accueil", "Bienvenue 👋"))

# 🧪 Mode démo (fallback)
mode_demo = st.sidebar.checkbox("🧪 Activer le mode démo (offline)", value=False)
mode_label = "Démo" if mode_demo else "IA réelle"
st.caption(f"🧬 Mode : {mode_label}")

# 🩺 Sélection du médecin
st.sidebar.markdown("## 🩺 Médecin référent")
if "Médecin" in df.columns:
    medecin_id = st.sidebar.selectbox("👨‍⚕️ Sélectionnez votre profil :", df["Médecin"].dropna().unique())
else:
    default_col = df.columns[0] if len(df.columns) > 0 else "Médecin"
    medecin_id = st.sidebar.selectbox("👨‍⚕️ Profil :", df[default_col].dropna().unique())

# ➕ Ajout de la colonne Résumé IA si absente
if "Résumé IA" not in df.columns:
    df["Résumé IA"] = ""

# 📋 Affichage des cas cliniques
st.subheader("📋 Cas cliniques")
st.dataframe(df, use_container_width=True)

# 🔁 Génération IA
if st.button("🔁 Générer les résumés IA"):
    st.info("📡 Résumés IA en cours de génération…")
    for i, row in df.iterrows():
        symptomes = row.get("Symptômes", "")
        if isinstance(symptomes, str) and symptomes.strip():
            resume = generer_resume(
                symptomes=symptomes,
                medecin_id=medecin_id,
                hf_token=HF_TOKEN,
                mode_demo=mode_demo
            )
            df.at[i, "Résumé IA"] = resume
    st.success("✅ Résumés IA générés.")

# 📥 Téléchargement CSV
if settings.get("export_csv", True):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Télécharger les cas enrichis (.csv)",
        data=csv,
        file_name="cas_cliniques_enrichis.csv",
        mime="text/csv"
    )
