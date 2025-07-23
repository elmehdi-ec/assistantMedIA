import requests

def generer_resume(symptomes: str, medecin_id: str, hf_token: str, mode_demo: bool = False) -> str:
    if mode_demo or hf_token is None:
        return f"(Simulation démo) {symptomes[:40]}..."

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Vous êtes médecin urgentiste.
Cas clinique :
Patient : {medecin_id}
Symptômes : {symptomes}

Fournissez un résumé médical concis avec hypothèse diagnostique et conduite à tenir.
"""

    payload = { "inputs": prompt.strip() }

    try:
        url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"].strip()
            else:
                return f"⚠️ Format inattendu reçu : {data}"
        else:
            return f"❌ Erreur {response.status_code} : {response.text[:100]}"
    except Exception as e:
        return f"❌ Erreur lors de l’appel IA : {str(e)}"
