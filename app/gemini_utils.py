import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def chamar_gemini(mensagem):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            "Você é a Dra. Ana, especialista em saúde feminina para mulheres de 40 a 50 anos. "
            "Seja empática, educada e humanizada em suas respostas. Use linguagem clara e acessível. "
            "Evite termos técnicos. Se a pergunta não for relacionada à saúde feminina, oriente a paciente gentilmente.\n\n"
            f"Pergunta: {mensagem}"
        )
        response = model.generate_content(prompt)
        return response.text or "Desculpe, não consegui entender. Poderia reformular?"
    except Exception as e:
        print("[Erro Gemini]", e)
        return "Desculpe, tive um problema para responder agora. Pode tentar mais tarde?"
