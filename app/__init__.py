from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import webhook

# Carregar variáveis do .env
load_dotenv()

app = Flask(__name__)
app.register_blueprint(webhook)

