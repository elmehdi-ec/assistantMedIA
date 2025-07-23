import os
import requests

def generer_resume(symptomes: str, medecin_id: str, hf_token: str, mode_demo: bool = False) -> str:
    if mode_demo or not hf_token:
        return "🧪 Résumé simulé : le patient présente des signes compatibles avec une pathologie respiratoire."

    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    prompt = (
        f"En tant que médecin {medecin_id}, analyse cliniquement le cas suivant "
        f"et rédige un résumé médical : {symptomes}"
    )
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        result = response.json()

        # ✅ Hugging Face retourne une LISTE contenant un dictionnaire avec 'generated_text'
        if isinstance(result, list) and "generated_text" in result[0]:
            texte = result[0]["generated_text"].strip()
            return texte if texte else "⚠️ Résumé vide — réponse IA reçue mais non exploitable."
        else:
            return "⚠️ Résumé non reçu — réponse inattendue du moteur IA."
    except Exception as e:
        return f"❌ Erreur lors de l’appel IA : {str(e)}"
