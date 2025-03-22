from flask import Blueprint, request, jsonify
import sqlite3
from app.gemini_utils import chamar_gemini
from app.whatsapp_utils import send_message_to_whatsapp
from app.db_utils import init_db
import os
from dotenv import load_dotenv  # ✅ Adicionado

# Carregar variáveis do .env
load_dotenv()  # ✅ Adicionado

webhook = Blueprint("webhook", __name__)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
print(f"🚀 VERIFY_TOKEN carregado: {VERIFY_TOKEN}")  # 👈 Adicionando esse print

@webhook.route("/webhook", methods=["GET", "POST"])
def handle_webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        if verify_token == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification token mismatch", 403

    data = request.json
    if not data.get("entry"): return jsonify({"status": "ignored"}), 200

    changes = data["entry"][0].get("changes", [])
    if not changes or "messages" not in changes[0]["value"]:
        return jsonify({"status": "ignored"}), 200

    message = changes[0]["value"]["messages"][0]
    if message["type"] != "text":
        return jsonify({"status": "ignored"}), 200

    numero = message["from"]
    mensagem = message["text"]["body"].lower().strip()

    conn = sqlite3.connect("consultas.db")
    cursor = conn.cursor()
    usuario = cursor.execute("SELECT * FROM usuarios WHERE numero = ?", (numero,)).fetchone()

    if not usuario:
        resposta = ("Olá! Eu sou a Dra. Ana, especialista em saúde feminina para mulheres de 40 a 50 anos. "
                    "Como posso ajudar você hoje? 😊\n"
                    "Escolha um plano:\n"
                    "1. 1 pergunta + 1 tréplica: R$ 50\n"
                    "2. 2 perguntas + 1 tréplica cada: R$ 80\n"
                    "3. 3 perguntas + 1 tréplica cada: R$ 120\n"
                    "Digite o número do plano (1, 2 ou 3).")
        cursor.execute("INSERT INTO usuarios (numero, plano, perguntas_restantes, treplicas_restantes) VALUES (?, 0, 0, 0)", (numero,))
    else:
        plano, perguntas, treplicas = usuario[1], usuario[2], usuario[3]
        if plano == 0 or (perguntas == 0 and treplicas == 0):
            if mensagem in ["1", "2", "3"]:
                plano = int(mensagem)
                cursor.execute("UPDATE usuarios SET plano = ?, perguntas_restantes = ?, treplicas_restantes = ? WHERE numero = ?",
                               (plano, plano, plano, numero))
                resposta = "Plano escolhido! Simule o pagamento com 'pagar'."
            else:
                resposta = "Por favor, escolha um plano válido (1, 2 ou 3)."
        elif mensagem == "pagar":
            resposta = "Pagamento confirmado! Agora você pode fazer sua pergunta. 😊"
        elif perguntas > 0:
            resposta_gemini = chamar_gemini(mensagem)
            resposta = f"Olá! Entendi sua dúvida. {resposta_gemini}\nSe precisar de mais detalhes, é só me perguntar. 😊"
            cursor.execute("UPDATE usuarios SET perguntas_restantes = ? WHERE numero = ?", (perguntas - 1, numero))
        elif treplicas > 0:
            resposta_gemini = chamar_gemini(mensagem)
            resposta = f"{resposta_gemini}\nFoi um prazer ajudar você! Cuide-se! 😊"
            cursor.execute("UPDATE usuarios SET treplicas_restantes = ? WHERE numero = ?", (treplicas - 1, numero))
        else:
            resposta = ("Você usou todas as perguntas e tréplicas. Escolha outro plano:\n"
                        "1. 1 pergunta + 1 tréplica: R$ 50\n"
                        "2. 2 perguntas + 1 tréplica cada: R$ 80\n"
                        "3. 3 perguntas + 1 tréplica cada: R$ 120")

    conn.commit()
    conn.close()
    send_message_to_whatsapp(numero, resposta)
    return jsonify({"status": "success"}), 200

# Inicializar banco ao carregar o app
init_db()

