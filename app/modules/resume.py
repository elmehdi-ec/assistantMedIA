import requests

def generer_resume(symptomes: str, medecin_id: str, hf_token: str, mode_demo: bool = False) -> str:
    if mode_demo or hf_token is None:
        return f"(Simulation démo) {symptomes[:40]}..."

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    # 🔎 Construction du prompt pour Mixtral
    prompt = f"""
Vous êtes un médecin urgentiste.
Voici le cas clinique :
Patient : {medecin_id}
Symptômes : {symptomes}

Donnez un résumé synthétique médical, avec hypothèse diagnostique et conduite à tenir.
"""

    payload = {
        "inputs": prompt.strip()
    }

    try:
        # ✅ URL corrigée vers modèle Mixtral actif
        url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            data = response.json()

            # 🔍 Extraction du texte généré
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"].strip()
            else:
                return f"⚠️ Format inattendu reçu : {str(data)}"
        else:
            return f"❌ Erreur {response.status_code} : {response.text[:120]}"
    except Exception as e:
        return f"❌ Erreur lors de l’appel IA : {str(e)}"
