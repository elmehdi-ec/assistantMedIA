import os
import requests

def generer_resume(symptomes, medecin_id, hf_token, mode_demo=False):
    if mode_demo or not hf_token:
        return "🧪 Résumé simulé : le patient présente des signes compatibles avec une pathologie respiratoire."

    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    prompt = f"En tant que médecin {medecin_id}, résume cliniquement ce cas : {symptomes}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        result = response.json()

        # ✅ Correction : Hugging Face retourne une LISTE avec un champ "generated_text"
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return "⚠️ Résumé vide ou inattendu — modèle IA n’a pas répondu comme prévu."
    except Exception as e:
        return f"❌ Erreur lors de l’appel IA : {str(e)}"
