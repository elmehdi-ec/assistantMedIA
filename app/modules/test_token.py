import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")
url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
payload = {
    "inputs": "Résumé clinique d’un patient adulte avec fièvre, toux sèche et essoufflement"
}

response = requests.post(url, headers=headers, json=payload, timeout=30)
print("🔎 Réponse brute :", response.json())
