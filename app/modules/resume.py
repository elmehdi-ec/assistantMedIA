import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 🔁 Chargement une seule fois du modèle Flan-T5 Base
MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# ⚙️ Détection de l'environnement (GPU ou CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generer_resume(symptomes: str, medecin_id: str, hf_token=None, mode_demo: bool = False) -> str:
    """
    Génère un résumé clinique en français à partir des symptômes du patient.
    Utilise le modèle local Flan-T5 Base. Le paramètre hf_token est ignoré.
    """
    if mode_demo:
        return f"(Mode démo actif) {symptomes[:40]}..."

    # 🧠 Prompt simplifié pour amélioration de la compréhension par le modèle
    prompt = (
        f"Un patient de sexe inconnu nommé {medecin_id} présente les symptômes suivants : {symptomes}.\n"
        f"Quels sont l'hypothèse diagnostique, la conduite à tenir et les examens complémentaires recommandés ?"
    )

    try:
        # ⛓️ Préparation des entrées
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=256)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # 🧪 Génération du texte
        outputs = model.generate(**inputs, max_new_tokens=100)
        texte = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return texte.strip()

    except Exception as e:
        return f"❌ Erreur IA : {str(e)}"
