import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Carregar chave da API do Gemini
API_KEY = os.getenv("GEMINI_API_KEY")

# Criação do cliente Gemini
client = OpenAI(api_key=API_KEY)

def chamar_gemini(pergunta: str) -> str:
    prompt = (
        "Você é a Dra. Ana, uma médica experiente, gentil e atenciosa, especializada em saúde feminina "
        "de mulheres com idade entre 40 e 50 anos. Responda de forma clara, empática e baseada em evidências "
        "científicas. Mantenha sempre o contexto da conversa. "
        f"\n\nPergunta da paciente:\n{pergunta}"
    )

    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ou gemini-pro se estiver usando VertexAI
            messages=[{"role": "user", "content": prompt}]
        )
        return resposta.choices[0].message.content.strip()

    except Exception as e:
        print(f"[ERRO Gemini]: {e}")
        return "Desculpe, houve um problema ao tentar responder sua pergunta. Tente novamente em instantes."

