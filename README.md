# 🇲🇦 Assistant Médical IA — Résumé Clinique Multilingue  
**Outil de soutien à la décision médicale** basé sur Streamlit & Hugging Face 🤖

> 🔍 *Un assistant intelligent pour les professionnels de santé marocains, conçu pour améliorer le triage des patients et le raisonnement clinique.*

## 🇬🇧 Medical AI Assistant — Multilingual Clinical Summarizer  
**Decision-support tool** powered by Streamlit & Hugging Face 🤖

> 🔍 *An intelligent assistant designed for healthcare professionals, focused on streamlining triage and enhancing clinical reasoning.*

---

## 🎯 Objectif / Purpose

- 🩺 Aider à la synthèse clinique des symptômes en langage médical  
- 🌍 Soutenir plusieurs langues (Français, Anglais, Arabe)  
- ⚙️ S’adapter au profil médecin (langue, spécialité, mode démo)  
- 🧠 Fournir un résumé IA via modèle Hugging Face  
- 📡 Fonctionne en local ou en ligne via Streamlit Cloud  

---

## 🚀 Fonctionnalités / Features

| Fonction / Feature | Description |
|---------------------|-------------|
| 🤖 Résumé IA         | Génération automatique à partir de symptômes |
| 👤 Profils médecins | Configuration par YAML : langue, spécialité |
| 🧪 Mode démo         | Fonctionne sans appel API Hugging Face |
| 🔐 Sécurité          | Aucun token exposé — configuration via `.env` ou secrets |
| 📤 Export            | Résumés téléchargeables au format CSV |

---

## 🔧 Installation / Setup

```bash
# Clone le projet
git clone https://github.com/elmehdi-ec/assistantMedIA.git
cd assistantMedIA

# Installe les dépendances
pip install -r requirements.txt

# Lance l'application
streamlit run app/app.py
```

---

## 🔐 Token IA (Hugging Face)

### 🖥️ Local `.env` file:
```txt
HF_TOKEN=hf_abc123...
```

### 🌐 Streamlit Cloud Secrets:
- Open your app’s Settings → Secrets
- Add: `HF_TOKEN = hf_abc123...`

---

## 🧠 Fichiers importants / Key files

- `data/cas_simules.csv` — Cas cliniques simulés  
- `config/medecins.yaml` — Profils et préférences médecins  
- `modules/resume.py` — Moteur IA sécurisé pour les résumés  
- `.gitignore` — Protège `.env` et fichiers sensibles  

---

## 🧪 Mode Démo (offline testing)

- Activez “Mode démo” dans la barre latérale  
- Résumés simulés générés localement  
- Utile pour les tests ou environnements sans internet  

---

## 📸 Capture d’écran / Screenshot (à ajouter)

*Ajoutez ici un aperçu du tableau Streamlit avec résumés IA.*

---

## 💡 Roadmap / Évolution

- 🔄 Migration vers Mistral / Bloomz  
- 📱 Version mobile simplifiée  
- 🧾 Export PDF patient  
- 🔐 Authentification médecin  

---
