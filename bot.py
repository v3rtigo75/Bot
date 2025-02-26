from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Respuestas predefinidas del bot
RESPUESTAS = {
    "hola": "¡Hola! ¿En qué puedo ayudarte hoy?",
    "adios": "¡Hasta luego! Si necesitas algo más, no dudes en contactarnos.",
    "ayuda": "Claro, estoy aquí para ayudarte. ¿Qué problema tienes?",
    "default": "Lo siento, no entendí eso. ¿Podrías intentarlo de nuevo?"
}

@app.route('/')
def home():
    # Mensaje de bienvenida para la ruta raíz
    return "Bienvenido al bot de atención al cliente. Usa la ruta /chat para interactuar."

@app.route('/chat', methods=['POST'])
def chat():
    # Obtener el mensaje del usuario
    user_message = request.json.get('mensaje', '').lower()
    
    # Buscar una respuesta adecuada
    response = RESPUESTAS.get(user_message, RESPUESTAS['default'])
    
    # Devolver la respuesta como JSON
    return jsonify({"respuesta": response})

if __name__ == '__main__':
    # Usa el puerto proporcionado por Render o el puerto 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
