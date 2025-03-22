from flask import Blueprint, request, jsonify
import sqlite3
from app.gemini_utils import chamar_gemini
from app.whatsapp_utils import send_message_to_whatsapp
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
    texto_usuario = message["text"]["body"].strip()

    # Enviar a mensagem diretamente para o Gemini
    prompt_base = (
        "Você é a Dra. Ana, uma médica especializada em saúde feminina de mulheres entre 40 e 50 anos. "
        "Responda de forma atenciosa, cuidadosa e mantendo o contexto da conversa anterior, se houver. "
        "Mensagem da paciente: "
    )
    resposta = chamar_gemini(f"{prompt_base} {texto_usuario}")

    # Enviar a resposta de volta pelo WhatsApp
    send_message_to_whatsapp(numero, resposta)

    return jsonify({"status": "success"}), 200



