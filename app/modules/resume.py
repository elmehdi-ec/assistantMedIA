import requests

def generer_resume(symptomes: str, medecin_id: str, hf_token: str, mode_demo: bool = False) -> str:
    if mode_demo or hf_token is None:
        return f"(Démo) Résumé simulé : {symptomes[:40]}..."

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Un patient nommé {medecin_id} présente les symptômes suivants : {symptomes}.
Rédigez un résumé médical en français comprenant :
- Hypothèse diagnostique
- Conduite à tenir
- Examens complémentaires
"""

    try:
        response = requests.post(
            url = "https://api-inference.huggingface.co/models/google/flan-t5-base",
            headers=headers,
            json={"inputs": prompt.strip()},
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"].strip()
            else:
                return f"⚠️ Format inattendu : {data}"
        else:
            return f"❌ Erreur {response.status_code} : {response.text[:100]}"

    except Exception as e:
        return f"❌ Erreur IA : {str(e)}"
