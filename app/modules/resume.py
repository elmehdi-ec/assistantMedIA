import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Chargement unique du modèle Flan-T5 Base
MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Envoi sur GPU si dispo, sinon CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generer_resume(symptomes: str, medecin_id: str, hf_token=None, mode_demo: bool = False) -> str:
    """
    Génère un résumé clinique en local avec le modèle Flan-T5 Base.
    hf_token est ignoré (IA locale).
    """
    if mode_demo:
        return f"(Démo) Résumé simulé : {symptomes[:40]}..."

    prompt = (
        f"Vous êtes médecin urgentiste.\n"
        f"Patient : {medecin_id}\n"
        f"Symptômes : {symptomes}\n\n"
        f"Rédigez un résumé médical synthétique en français incluant :\n"
        f"- Hypothèse diagnostique\n"
        f"- Conduite à tenir\n"
        f"- Examens complémentaires"
    )

    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=256)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        outputs = model.generate(**inputs, max_new_tokens=100)
        texte = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return texte.strip()
    except Exception as e:
        return f"❌ Erreur IA : {str(e)}"
