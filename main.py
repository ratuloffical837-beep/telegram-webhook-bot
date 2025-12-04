from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
import logging
from config import BOT_TOKEN
from models import save_user, save_message

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

# Telegram dispatcher setup
from telegram.ext import Dispatcher
dispatcher = Dispatcher(bot, None, workers=4)

# Basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Message handler
def handle_message(update: Update, context):
    user_id = update.effective_user.id
    text = update.message.text

    save_user(user_id)
    save_message(user_id, text)

    update.message.reply_text("Message received!")

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Webhook receiver
@app.route('/', methods=['POST'])
def webhook():
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, bot)
    dispatcher.process_update(update)
    return "OK", 200

# Health check
@app.route('/', methods=['GET'])
def home():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
