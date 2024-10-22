import logging
import os

from dotenv import load_dotenv
from openai import OpenAI  # This is new!
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()  # take environment variables from .env.

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])  # This is new!
tg_bot_token = os.getenv("TG_BOT_TOKEN")


messages = [
    {"role": "system", "content": "You are a helpful assistant that answers questions."}
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


application = ApplicationBuilder().token(tg_bot_token).build()

start_handler = CommandHandler("start", start)
application.add_handler(start_handler)

application.run_polling()
