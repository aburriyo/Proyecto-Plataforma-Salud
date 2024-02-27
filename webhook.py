import os
from dotenv import load_dotenv
from twilio.rest import Client
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# URL de la API de CodeGPT
url = "https://api-beta.codegpt.co/api/v1/chat/completions"

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        body = request.form.get('Body')
        sender = request.form.get('From')
        
        # Llamamos a la función para obtener la respuesta de CodeGPT
        codegpt_response = get_codegpt_response(body)
        
        # Enviamos la respuesta de CodeGPT como mensaje a través de Twilio
        send_twilio_response(sender, codegpt_response)
        
        # Retornamos la respuesta de CodeGPT
        response = {
            'body': codegpt_response,
            'sender': sender
        }
        return jsonify(response), 200
    else:
        return "Método no permitido", 405

def get_codegpt_response(message):
    payload = {
        "agentId": "330ae7bb-a10e-4df5-a7ee-1c9a92c081aa",
        "messages": message,
        "format": "json",
        "stream": False
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
            return response.json().get('message')
    else:
        return "No se pudo obtener respuesta de CodeGPT"

def send_twilio_response(to, message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        to=to 
    )
    print(to)
    print(message.sid)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
