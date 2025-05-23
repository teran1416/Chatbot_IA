const venom = require('venom-bot');
const axios = require('axios');

// Catálogo con imágenes reales
const autos = {
  "chevrolet spark": "https://acnews.blob.core.windows.net/imgnews/medium/NAZ_1717278aeb7e4c4f9a37b6a90b173a6d.jpg",
  "toyota prado": "https://toyotadecolombia.com.co/wp-content/uploads/2021/07/prado-2021.png",
  "mazda cx-30": "https://mazda.com.co/wp-content/uploads/2021/11/CX-30-LUXURY.png",
  "suzuki vitara": "https://suzukiauto.com.co/wp-content/uploads/2021/11/Vitara-negro.png",
  "chevrolet aveo": "https://noticias.autocosmos.hn/resizer/tU-V47smuQyDjf4Yh_jYhT6trYY=/fit-in/1200x900/smart/cloudfront-us-east-1.images.arcpublishing.com/gruponacion/BYAZFFLC6VD23D7GZXK3TYYJH4.jpg"
};

venom
  .create({
    session: 'whatsapp-chatbot',
    headless: false,
    useChrome: true
  })
  .then((client) => start(client))
  .catch((erro) => {
    console.log(erro);
  });

function start(client) {
  client.onMessage(async (message) => {
    if (message.body && message.isGroupMsg === false) {
      console.log("Mensaje recibido:", message.body);

      // Enviar la pregunta al servidor Python
      try {
        const respuestaIA = await axios.post('http://localhost:5000/ia', {
          pregunta: message.body
        });

        const respuesta = respuestaIA.data.respuesta;
        await client.sendText(message.from, respuesta);

        // Detectar si mencionó un auto conocido
        const mensaje = message.body.toLowerCase();
        for (const nombre in autos) {
          if (mensaje.includes(nombre)) {
            await client.sendImage(
              message.from,
              autos[nombre],
              nombre.replace(/\s+/g, '_'),
              `Aquí tienes una imagen del ${nombre.charAt(0).toUpperCase() + nombre.slice(1)} 🚗`
            );
            break;
          }
        }
      } catch (err) {
        console.error("Error al contactar con IA:", err.message);
        await client.sendText(message.from, "Lo siento, hubo un error procesando tu mensaje.");
      }
    }
  });
}
