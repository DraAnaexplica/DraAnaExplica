import requests
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

def send_message_to_whatsapp(to_number, message):
    url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print(f"[✅ Mensagem enviada com sucesso para {to_number}]")
    else:
        print(f"[❌ Erro ao enviar mensagem] Status: {response.status_code}")
        print(f"[❌ Resposta da API] {response.text}")

    return response.status_code == 200

