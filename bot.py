from flask import Flask, request, jsonify
import os
from flask_cors import CORS  # Importa CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Respuestas predefinidas del bot
RESPUESTAS = {
    "hola": "¡Hola! ¿En qué puedo ayudarte hoy?",
    "adios": "¡Hasta luego! Si necesitas algo más, no dudes en contactarnos.",
    "ayuda": "Claro, estoy aquí para ayudarte. ¿Qué problema tienes?",
    "default": "Lo siento, no entendí eso. ¿Podrías intentarlo de nuevo?"
}

@app.route('/')
def home():
    return "Bienvenido al bot de atención al cliente. Usa la ruta /chat para interactuar."

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('mensaje', '').lower()
    response = RESPUESTAS.get(user_message, RESPUESTAS['default'])
    return jsonify({"respuesta": response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
