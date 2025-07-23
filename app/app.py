import streamlit as st
from transformers import pipeline
import os

# Title and description
st.set_page_config(page_title="AssistantMedIA", page_icon="🩺")
st.title("🩺 Assistant IA Clinique Multilingue")
st.write("Posez vos questions médicales dans la langue de votre choix.")

# Retrieve Hugging Face token
HF_TOKEN = os.getenv("HF_TOKEN", "your_huggingface_token_here")  # Replace with secure method if needed

# Display token in sidebar (masked for security)
st.sidebar.write("🔐 HF_TOKEN =", HF_TOKEN[:4] + "..." + HF_TOKEN[-4:])

# Language selection
language = st.selectbox("Choisissez la langue", ["fr", "en", "es", "de", "ar"])

# Load model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", token=HF_TOKEN)

generator = load_model()

# User input
user_input = st.text_area("Votre question médicale")

# Generate response
if st.button("Répondre"):
    with st.spinner("Analyse en cours..."):
        prompt = f"[{language}] {user_input}"
        response = generator(prompt, max_new_tokens=200)[0]["generated_text"]
        st.success("Réponse générée :")
        st.write(response)
