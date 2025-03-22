# app/gemini_utils.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Carregar chave da API do Gemini
API_KEY = os.getenv("GEMINI_API_KEY")

# Configurar cliente Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

def chamar_gemini(pergunta: str) -> str:
    prompt = (
        "Você é a Dra. Ana, uma médica experiente, gentil e atenciosa, especializada em saúde feminina "
        "de mulheres com idade entre 40 e 50 anos. Responda de forma clara, empática e baseada em evidências "
        "científicas. Mantenha sempre o contexto da conversa. "
        f"\n\nPergunta da paciente:\n{pergunta}"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERRO Gemini]: {e}")
        return "Desculpe, houve um erro ao tentar responder. Tente novamente em instantes."





