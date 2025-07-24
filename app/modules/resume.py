import requests

def generer_resume(symptomes: str, medecin_id: str, hf_token: str, mode_demo: bool = False) -> str:
    if mode_demo or hf_token is None:
        return f"(Mode démo actif) Résumé simulé : {symptomes[:40]}..."

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    # 🧠 Prompt médical structuré pour Bloomz
    prompt = f"""
Vous êtes médecin urgentiste.
Voici un cas clinique :
Patient : {medecin_id}
Symptômes : {symptomes}

Rédigez un résumé médical synthétique en français incluant :
- Hypothèse diagnostique
- Conduite à tenir
- Examens complémentaires recommandés
"""

    payload = { "inputs": prompt.strip() }

    try:
        # ✅ Modèle stable et accessible via Hugging Face Inference API
        url = "https://api-inference.huggingface.co/models/bigscience/bloomz"
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"].strip()
            else:
                return f"⚠️ Format inattendu : {data}"
        else:
            return f"❌ Erreur {response.status_code} : {response.text[:100]}"
    except Exception as e:
        return f"❌ Erreur lors de l’appel IA : {str(e)}"
