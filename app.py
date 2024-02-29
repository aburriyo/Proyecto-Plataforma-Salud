from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse

# Importa la clase CodeGPTPlus desde tu librería
from judini import CodeGPTPlus

app = FastAPI()

# Configura tu cliente de CodeGPTPlus
codegpt = CodeGPTPlus(api_key='XXXX-XXXX-XXXX-XXXX', org_id='XXXX-XXXX-XXXX-XXXX')
AGENT_ID = "XXXX-XXXX-XXXX-XXXX"

@app.post("/hook")
async def chat(From: str = Form(...), Body: str = Form(...)):
    # Prepara el mensaje para enviar a CodeGPTPlus
    messages = [{"role": "user", "content": Body}]
    
    # Obtiene la respuesta de CodeGPTPlus
    chat_response = codegpt.chat_completion(agent_id=AGENT_ID, messages=messages)
    
    # Imprime la respuesta para debug
    print(chat_response)  # Agrega esta línea para debug
    
    try:
        # Asume que chat_response es un diccionario y accede a la respuesta
        response_text = chat_response
    except TypeError as e:
        # Manejo de error si chat_response no es un diccionario o la estructura es diferente
        print(f"Error al procesar la respuesta: {e}")
        response_text = "Ocurrió un error al procesar tu mensaje."
    
    # Crea la respuesta de Twilio con el texto generado
    response = MessagingResponse()
    msg = response.message(response_text)
    
    return Response(content=str(response), media_type="application/xml")
