import requests
import yaml

# 🔐 Chargement du token Hugging Face
def charger_token():
    try:
        with open("config/token.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)["huggingface_token"]
    except Exception:
        return None

HF_TOKEN = charger_token()

# 👤 Chargement du profil médecin
def charger_profil(medecin_id):
    try:
        with open("config/medecins.yaml", "r", encoding="utf-8") as f:
            profils = yaml.safe_load(f)
        return profils.get(medecin_id, {"langue": "fr"})
    except Exception:
        return {"langue": "fr"}

# 🧠 Fonction principale : résumé clinique multilingue
def generer_resume(symptomes: str, medecin_id: str, mode_demo: bool = False) -> str:
    profil = charger_profil(medecin_id)
    langue = profil.get("langue", "fr")

    if mode_demo or HF_TOKEN is None:
        return f"🧠 [DEMO-{langue}] Résumé simulé : {symptomes}"

    # 🎯 Création du prompt adapté
    if langue == "fr":
        prompt = f"Tu es une IA médicale francophone. Résume ces symptômes : {symptomes}"
    elif langue == "ar":
        prompt = f"أنت مساعد طبي. لخص الأعراض التالية بطريقة سريرية: {symptomes}"
    else:
        prompt = f"You are a clinical AI. Summarize these symptoms: {symptomes}"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    url = "https://api-inference.huggingface.co/models/google/medgemma-4b-it"
    payload = {"inputs": prompt}

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"].strip()
            else:
                return f"⚠️ Réponse inattendue : {result}"
        else:
            return f"⛔ Erreur API ({response.status_code}) : {response.text}"
    except Exception as e:
        return f"⚠️ Exception IA : {str(e)}"
