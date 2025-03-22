# app/routes.py

from flask import Blueprint, request, jsonify
import sqlite3
from app.gemini_utils import chamar_gemini
from app.whatsapp_utils import send_message_to_whatsapp
from app.db_utils import init_db
import os
from dotenv import load_dotenv

load_dotenv()

webhook = Blueprint("webhook", __name__)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@webhook.route("/webhook", methods=["GET", "POST"])
def handle_webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        if verify_token == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification token mismatch", 403

    data = request.json
    if not data.get("entry"):
        return jsonify({"status": "ignored"}), 200

    changes = data["entry"][0].get("changes", [])
    if not changes or "messages" not in changes[0]["value"]:
        return jsonify({"status": "ignored"}), 200

    message = changes[0]["value"]["messages"][0]
    if message["type"] != "text":
        return jsonify({"status": "ignored"}), 200

    numero = message["from"]
    texto_usuario = message["text"]["body"].strip().lower()

    conn = sqlite3.connect("consultas.db")
    cursor = conn.cursor()

    # Tenta achar o usuário no banco
    usuario = cursor.execute("SELECT * FROM usuarios WHERE numero = ?", (numero,)).fetchone()

    if not usuario:
        # Novo usuário -> gerar saudação via IA
        greeting_prompt = (
            "Você é a Dra. Ana, uma médica experiente, gentil e atenciosa. "
            "Uma nova paciente acabou de entrar em contato pela primeira vez. "
            "Por favor, cumprimente-a de forma amigável e natural, sem repetir sempre as mesmas frases, "
            "e mostre disponibilidade para ouvir as preocupações dela."
        )
        saudacao_inicial = chamar_gemini(greeting_prompt)
        resposta = saudacao_inicial

        # Insere o usuário no banco, sem planos nem perguntas
        cursor.execute(
            "INSERT INTO usuarios (numero, plano, perguntas_restantes, treplicas_restantes) VALUES (?, 0, 0, 0)",
            (numero,)
        )
    else:
        # Usuário existente -> conversa normal com a IA
        resposta_gemini = chamar_gemini(texto_usuario)
        resposta = resposta_gemini

    conn.commit()
    conn.close()

    # Enviar a resposta de volta pelo WhatsApp
    send_message_to_whatsapp(numero, resposta)

    return jsonify({"status": "success"}), 200

# Inicializar banco ao carregar o app
init_db()





