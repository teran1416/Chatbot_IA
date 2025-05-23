from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = Flask(__name__)
CORS(app)

# Catálogo de autos
auto_info = {
    "chevrolet spark": {
        "descripcion": "Auto compacto, ideal para ciudad. Muy económico y fácil de parquear.",
        "imagen": "https://acnews.blob.core.windows.net/imgnews/medium/NAZ_1717278aeb7e4c4f9a37b6a90b173a6d.jpg"
    },
    "toyota prado": {
        "descripcion": "SUV robusta, potente, perfecta para viajes largos y terrenos difíciles.",
        "imagen": "https://toyotadecolombia.com.co/wp-content/uploads/2021/07/prado-2021.png"
    },
    "mazda cx-30": {
        "descripcion": "Crossover moderno, elegante y cómodo. Excelente para uso familiar.",
        "imagen": "https://mazda.com.co/wp-content/uploads/2021/11/CX-30-LUXURY.png"
    },
    "suzuki vitara": {
        "descripcion": "SUV compacta, confiable, buena para ciudad y campo.",
        "imagen": "https://suzukiauto.com.co/wp-content/uploads/2021/11/Vitara-negro.png"
    },
    "chevrolet aveo": {
        "descripcion": "Sedán clásico, cómodo, ideal para quienes buscan rendimiento a buen precio.",
        "imagen": "https://noticias.autocosmos.hn/resizer/tU-V47smuQyDjf4Yh_jYhT6trYY=/fit-in/1200x900/smart/cloudfront-us-east-1.images.arcpublishing.com/gruponacion/BYAZFFLC6VD23D7GZXK3TYYJH4.jpg"
    }
}

# Crear el menú en texto plano
menu_autos = ""
for nombre, datos in auto_info.items():
    menu_autos += f"- {nombre.title()}: {datos['descripcion']}\n"

# Template para LangChain
template = """
Eres un asesor profesional de ventas de autos. Alguien te hará una pregunta específica.

Responde de forma clara y profesional, solo con la información necesaria.
Incluye una breve descripción del auto si lo mencionan y el enlace a su imagen si corresponde.

Mensaje del cliente: {input}
Tu respuesta:
"""

prompt = PromptTemplate(
    input_variables=["input"],
    template=template,
)

# Usar llama3 como LLM
llm = Ollama(model="llama3")
chain = LLMChain(llm=llm, prompt=prompt)

@app.route('/ia', methods=['POST'])
def responder():
    data = request.get_json()
    pregunta = data.get("pregunta", "").lower()

    # Detectar si es un saludo o solicitud general
    if any(p in pregunta for p in ["hola", "buenas", "catálogo", "ver autos", "mostrar autos", "autos disponibles"]):
        respuesta = f"""¡Hola! Soy tu asesor virtual de autos 🚗

Aquí tienes nuestro catálogo actual:
{menu_autos}

Dime si alguno te interesa o si deseas una recomendación personalizada.
"""
    else:
        respuesta = chain.run(input=pregunta)

    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    app.run(port=5000)
