import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

def chamar_gemini(pergunta: str) -> str:
    prompt = (
        "Você é a Dra. Ana, uma médica experiente, gentil e atenciosa, especializada em saúde feminina "
        "de mulheres com idade entre 40 e 50 anos. Responda de forma clara, empática e baseada em evidências "
        "científicas. Mantenha sempre o contexto da conversa. "
        f"\n\nPergunta da paciente:\n{pergunta}"
    )

    try:
        print(f"[DEBUG Gemini] API_KEY está carregada? {'SIM' if API_KEY else 'NÃO'}")
        print(f"[DEBUG Gemini] Prompt enviado:\n{prompt}")

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"[ERRO Gemini]: {e}")
        return "Desculpe, houve um erro ao tentar responder. Tente novamente em instantes."



