import streamlit as st
import pandas as pd
import os
import configparser
import requests

# ---------- Configuration ----------
st.set_page_config(page_title="Assistant IA clinique", layout="wide")
config = configparser.ConfigParser()
config.read('config.ini')
HF_TOKEN = config.get("default", "HF_TOKEN", fallback=None)

# ---------- Fonctions ----------
def load_data():
    data = pd.DataFrame([
        {"Nom": "Ahmed", "Âge": 65, "Sexe": "Homme", "Symptômes": "Fièvre, toux, essoufflement", "Gravité": 8},
        {"Nom": "Salma", "Âge": 32, "Sexe": "Femme", "Symptômes": "Céphalée, douleur oreille", "Gravité": 3},
        {"Nom": "Youssef", "Âge": 74, "Sexe": "Homme", "Symptômes": "Confusion, chute récente", "Gravité": 9},
        {"Nom": "Imane", "Âge": 19, "Sexe": "Femme", "Symptômes": "Maux gorge, fièvre", "Gravité": 4},
    ])
    return data

def generer_resume(symptomes):
    prompt = f"Voici un résumé médical des symptômes suivants : {symptomes}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 100}
    }
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-large",
            headers=headers,
            json=payload,
            timeout=20
        )
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            return f"❌ Erreur API: {response.status_code}"
    except Exception as e:
        return f"⚠️ Erreur : {e}"

# ---------- UI ----------
st.title("📋 Cas cliniques")
df = load_data()
mode_demo = st.sidebar.checkbox("🎛️ Activer le mode démo (offline)", value=False)

profil_medecin = st.sidebar.selectbox("🧑‍⚕️ Profil :", options=df["Nom"].unique())
st.markdown(f"### Bienvenue **{profil_medecin}** 🩺")

if HF_TOKEN:
    st.success(f"🔐 Token Hugging Face détecté. Début: `{HF_TOKEN[:8]}...`")
else:
    st.warning("⚠️ Aucun HF_TOKEN détecté dans le fichier `config.ini`.")

# ---------- Table ----------
df_display = df.copy()
df_display["Résumé IA"] = ""

if st.button("🧠 Générer les résumés IA"):
    if mode_demo or not HF_TOKEN:
        df_display["Résumé IA"] = df["Symptômes"].apply(lambda x: "Mode démo — résumé non généré")
    else:
        with st.spinner("⏳ Envoi des cas au moteur IA..."):
            df_display["Résumé IA"] = df["Symptômes"].apply(generer_resume)
        st.success("✅ Résumés IA générés.")

# ---------- Output ----------
st.dataframe(df_display)

# ---------- Export ----------
csv = df_display.to_csv(index=False).encode('utf-8')
st.download_button("📥 Télécharger les cas enrichis (.csv)", csv, "cas_cliniques.csv", "text/csv")
