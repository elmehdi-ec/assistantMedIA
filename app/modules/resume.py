import requests

def generer_resume(symptomes: str, medecin_id: str, hf_token: str, mode_demo: bool = False) -> str:
    if mode_demo or hf_token is None:
        return f"(Mode démo actif) Résumé simulé : {symptomes[:40]}..."

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    # 🧠 Prompt médical structuré pour BloomZ
    prompt = f"""
Un patient de sexe inconnu nommé {medecin_id} présente les symptômes suivants : {symptomes}.
Quels sont le diagnostic, la conduite à tenir et les examens complémentaires recommandés ?
"""

    payload = { "inputs": prompt.strip() }

    try:
        # ✅ Modèle gratuit via Inference API
        url = "https://api-inference.huggingface.co/models/bigscience/bloomz-560m"
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
