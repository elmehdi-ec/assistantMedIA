import requests

def generer_resume(symptomes: str, medecin_id: str, hf_token: str, mode_demo: bool = False) -> str:
    if mode_demo or hf_token is None:
        return f"(Fallback simulé) {symptomes[:40]}..."

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": f"Patient : {medecin_id}\nSymptômes : {symptomes}\n\nRésumé clinique synthétique :"
    }

    try:
        response = requests.post(
            url="https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            # Certains modèles renvoient une liste d'objets text
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"].strip()
            elif isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"].strip()
            elif isinstance(data, list) and "generated_text" in data[0].get("generated_token", {}):
                return data[0]["generated_token"]["generated_text"].strip()
            else:
                return f"❌ Format de réponse inattendu : {data}"
        else:
            return f"❌ Erreur {response.status_code} : {response.text[:100]}"
    except Exception as e:
        return f"❌ Erreur lors de l’appel IA : {str(e)}"
