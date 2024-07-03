from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import logging
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Configurar el logging para ver mensajes de depuración
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

ERROR_THRESHOLD = 30  # Umbral de error para la similitud (de 0 a 100)

# Cargar el archivo de intenciones
def load_intents():
    try:
        with open('intents.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error al cargar el archivo intents.json: {e}")
        return None

# Función para calcular la similitud y manejar la respuesta
def handle_response(text: str) -> str:
    intents = load_intents()
    if not intents:
        return "Lo siento, no puedo cargar mis respuestas en este momento."

    best_match = None
    best_score = 0
    
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            score = fuzz.ratio(pattern.lower(), text.lower())
            if score > best_score:
                best_score = score
                best_match = intent

    if best_score >= ERROR_THRESHOLD:
        response = best_match['responses']
        return response[0]  # Selecciona la primera respuesta de la lista (puedes modificar esto para seleccionar aleatoriamente)
    else:
        return "No entiendo. ¿Puedes repetir?"

# Token y nombre de usuario del bot
token = "7366210086:AAFAUrIwBrKRfxy29-PjF9wSqcEEYrhg8M0"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bienvenido! ¿En qué puedo ayudarte hoy?")

# Comando /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Puedes preguntarme cosas como: '¿Qué servicios ofrecen?' o '¿Cuál es su horario?'.")

# Comando /hacer_pedido
async def make_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = "https://example.com/make_order"  # Reemplaza con el enlace que deseas
    text = "¡Genial! ¿Qué deseas pedir? Haz clic en el siguiente enlace para realizar tu pedido: <a href='{}'>Realizar pedido</a>".format(link)
    await update.message.reply_text(text, parse_mode='HTML')

# Comando /contactar
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Claro! Puedes contactarnos a través de [tu correo electrónico o número de teléfono]. Estamos aquí para ayudarte.")

# Comando /conocenos
async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Somos un equipo de desarrolladores apasionados de crear soluciones innovadoras. Nuestro objetivo es brindarte la mejor experiencia posible.")

# Manejar mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    
    # Verificar si el mensaje comienza con "soy "
    if text.startswith("soy "):
        nombre = text[4:]  # Obtener el nombre del mensaje (eliminar "soy ")
        await update.message.reply_text(f"Encantado de conocerte, {nombre.capitalize()}!")

    else:
        response = handle_response(text)
        await update.message.reply_text(response, parse_mode='HTML')  # Añadir parse_mode='HTML' si es necesario
# Manejar errores
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update "{update}" caused error "{context.error}"')

# Inicializar el bot
if __name__ == '__main__':
    print('Iniciando bot...')
    app = Application.builder().token(token).build()
    
    # Añadir comandos
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('hacer_pedido', make_order))
    app.add_handler(CommandHandler('contactar', contact))
    app.add_handler(CommandHandler('conocenos', about_us))
    
    # Manejar mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Manejar errores
    app.add_error_handler(error)
    
    # Ejecutar el bot
    logger.info('Bot iniciado')
    app.run_polling(poll_interval=1, timeout=10)
