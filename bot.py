import requests
from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Respuestas predefinidas del bot
RESPUESTAS = {
    "hola": "¡Hola! ¿En qué puedo ayudarte hoy?",
    "adios": "¡Hasta luego! Si necesitas algo más, no dudes en contactarnos.",
    "ayuda": "Claro, estoy aquí para ayudarte. ¿Qué problema tienes?",
    "default": "Lo siento, no entendí eso. ¿Podrías intentarlo de nuevo?"
}

# Endpoint de la API de Qwen
QWEN_API_URL = "https://api.qwen.com/v1/chat"
API_KEY = "sk-ee011c67af7842ff8b1cb126f2ed2e1c"  # Reemplaza esto con tu API Key real

def consultar_a_qwen(mensaje):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": f"Eres un asistente especializado en atención al cliente. Responde de manera clara y profesional a la siguiente pregunta: {mensaje}",
        "max_tokens": 50
    }
    response = requests.post(QWEN_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        respuesta_generada = response.json().get("respuesta", "No pude procesar tu solicitud.")
        return filtrar_respuesta(respuesta_generada)
    else:
        return "Hubo un error al contactar con Qwen."

def filtrar_respuesta(respuesta_generada):
    """
    Filtra o ajusta la respuesta generada por Qwen para asegurar que sea adecuada.
    """
    # 1. Limitar la longitud de la respuesta
    if len(respuesta_generada) > 100:  # Si la respuesta es demasiado larga
        respuesta_filtrada = respuesta_generada[:100] + "..."
    else:
        respuesta_filtrada = respuesta_generada

    # 2. Asegurarse de que la respuesta sea profesional
    palabras_no_permitidas = ["grosería", "insulto", "ofensa"]  # Personaliza según tus necesidades
    for palabra in palabras_no_permitidas:
        if palabra in respuesta_filtrada.lower():
            respuesta_filtrada = "Lo siento, no puedo proporcionar una respuesta adecuada en este momento."

    # 3. Añadir un tono amigable (opcional)
    respuesta_filtrada = respuesta_filtrada + " 😊"

    return respuesta_filtrada

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('mensaje', '').lower()
    
    # Intentar responder con las respuestas predefinidas
    if user_message in RESPUESTAS:
        response = RESPUESTAS[user_message]
    else:
        # Si no hay respuesta predefinida, consultar a Qwen
        response = consultar_a_qwen(user_message)
    
    return jsonify({"respuesta": response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
