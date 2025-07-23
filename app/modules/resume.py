import os, requests

def generer_resume(symptomes, medecin_id, hf_token, mode_demo=False):
    if mode_demo or not hf_token:
        return "🧪 Mode démo activé — résumé simulé généré localement."

    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    prompt = f"En tant que médecin {medecin_id}, résume cliniquement les symptômes suivants : {symptomes}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        result = response.json()

        # 🔎 Debug log (désactivé en prod)
        print("✅ Réponse IA :", result)

        return result.get("generated_text", "⚠️ Résumé vide — vérifier réponse API.")
    except Exception as e:
        return f"❌ Erreur IA : {str(e)}"
