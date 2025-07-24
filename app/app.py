import streamlit as st
import pandas as pd
import yaml
from modules.resume import generer_resume

# ⚙️ Chargement des paramètres depuis settings.yaml
def charger_settings():
    try:
        with open("config/settings.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f).get("assistant", {})
    except Exception:
        return {}

settings = charger_settings()

# 📁 Chargement du CSV des cas cliniques
DATA_PATH = "data/cas_simules.csv"
try:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
except Exception:
    st.error("❌ Le fichier 'cas_simules.csv' est introuvable ou endommagé.")
    st.stop()

# 🎨 Configuration de la page
st.set_page_config(page_title=settings.get("nom_projet", "Assistant Médical IA"), layout="wide")
st.title("🧠 " + settings.get("nom_projet", "Assistant Médical IA"))
st.markdown(settings.get("message_accueil", "Bienvenue 👋"))

# 🧪 Mode démo local (optionnel)
mode_demo = st.sidebar.checkbox("🧪 Activer le mode démo", value=False)
mode_label = "Démo" if mode_demo else "IA locale"
st.caption(f"🧬 Mode : {mode_label}")

# 🩺 Sélection du médecin
st.sidebar.markdown("## 🩺 Médecin référent")
if "Médecin" in df.columns:
    medecin_id = st.sidebar.selectbox("👨‍⚕️ Sélectionnez votre profil :", df["Médecin"].dropna().unique())
else:
    medecin_id = st.sidebar.text_input("👨‍⚕️ Nom du médecin :", "Dr Elmehdi")

# ➕ Création de la colonne Résumé IA si absente
if "Résumé IA" not in df.columns:
    df["Résumé IA"] = ""

# 📋 Affichage du tableau
st.subheader("📋 Cas cliniques")
st.dataframe(df, use_container_width=True)

# 🔁 Génération des résumés IA
if st.button("🔁 Générer les résumés IA"):
    st.info("🧠 Génération locale en cours...")
    for i, row in df.iterrows():
        symptomes = row.get("Symptômes", "")
        if isinstance(symptomes, str) and symptomes.strip():
            try:
                resume = generer_resume(symptomes, medecin_id, hf_token=None, mode_demo=mode_demo)
            except Exception as e:
                resume = f"❌ Erreur de génération : {str(e)}"
            df.at[i, "Résumé IA"] = resume
    st.success("✅ Résumés IA générés.")

# 📥 Export du CSV enrichi
if settings.get("export_csv", True):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger les cas enrichis (.csv)",
        data=csv,
        file_name="cas_cliniques_enrichis.csv",
        mime="text/csv"
    )
