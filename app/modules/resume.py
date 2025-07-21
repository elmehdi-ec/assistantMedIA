import requests
import yaml
import os

# 📁 Charger le profil médecin
def charger_profil(medecin_id):
    try:
        with open("config/medecins.yaml", "r", encoding="utf-8") as file:
            profils = yaml.safe_load(file)
        return profils.get(medecin_id, {})
    except Exception:
        return {}

# 🧠 Générer le résumé IA
def generer_resume(symptomes, medecin_id, HF_TOKEN, mode_demo=False):
    profil = charger_profil(medecin_id)
    langue = profil.get("langue", "fr")
    specialite = profil.get("specialite", "médecine générale")

    # 💬 Prompt adapté
    prompt = (
        f"Tu es un médecin spécialiste en {specialite}. Résume les symptômes suivants en style clinique, en {langue} : {symptomes}"
    )

    # 🔁 Mode démo = réponse simulée
    if mode_demo:
        return f"[Résumé IA simulé en {langue}] : Patient présente {symptomes.lower()}."

    # 🔌 Appel API Hugging Face
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    try:
        url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            output = response.json()
            return output[0]["generated_text"]
        else:
            return f"[Fallback IA] Symptômes détectés : {symptomes}. Résumé manuel en cours."
    except Exception:
        return f"[⚠️ IA indisponible] Résumé simulé : {symptomes.lower()}"
