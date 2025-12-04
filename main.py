from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os

# ------------------------------
# Import config
# ------------------------------
from config import BOT_TOKEN, WEBHOOK_BASE

# ------------------------------
# Flask app
# ------------------------------
app = Flask(__name__)

# Telegram Bot instance
application = ApplicationBuilder().token(BOT_TOKEN).build()

# ------------------------------
# Bot Commands
# ------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running successfully on Render! 🚀")

# Add command handler
application.add_handler(CommandHandler("start", start))

# ------------------------------
# Telegram Webhook Receiver
# ------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    asyncio.run(application.process_update(update))
    return "OK", 200

# ------------------------------
# Home Route
# ------------------------------
@app.route("/")
def home():
    return "Bot is Live! 🎉"

# ------------------------------
# Main Entry Point
# ------------------------------
if __name__ == "__main__":
    # Build webhook URL
    webhook_url = f"{WEBHOOK_BASE}/webhook"
    print("Setting webhook to:", webhook_url)

    # Set Telegram Webhook
    asyncio.run(application.bot.set_webhook(webhook_url))

    # Run Flask App
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
