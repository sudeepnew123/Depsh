import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load bot token securely from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("DeepSeek bot is ready! Type anything.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    try:
        result = subprocess.check_output(['python3', 'inference/generate.py', '--prompt', prompt])
        await update.message.reply_text(result.decode().strip())
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"Error: {e.output.decode()}")
    except Exception as e:
        await update.message.reply_text(f"Unexpected error: {e}")

if BOT_TOKEN is None:
    print("Error: BOT_TOKEN not set. Please define it in your Render environment variables.")
else:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()