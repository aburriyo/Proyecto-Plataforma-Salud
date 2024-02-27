import os
from dotenv import load_dotenv
from twilio.rest import Client
import requests

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

if account_sid is None or auth_token is None:
    print("Importante! configurar las variables de entorno TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN en el archivo .env")
    exit()


webhook_url = 'https://webhook.site/15d716cb-4066-41ab-865b-a23650aabaf2'


response = requests.get(webhook_url)

if response.status_code == 200:
    # Obtener el contenido de la respuesta (los mensajes recibidos)
    messages = response.json()  
    print("Mensajes recibidos:")
    for message in messages:
        print("- De:", message.get('from'))  
        print("- Mensaje:", message.get('body')) 
        print()
else:
    print("Error al realizar la solicitud:", response.status_code)

# Enviar un mensaje a través de Twilio
message = client.messages.create(
    body='Hola',
    from_='whatsapp:+14155238886',
    to='whatsapp:+56942589424'
)

print(message.sid)
