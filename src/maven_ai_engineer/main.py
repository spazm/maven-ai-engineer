import logging
import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

load_dotenv()

tg_bot_token = os.getenv("TG_BOT_TOKEN")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    from .commands import chat, start

    application = ApplicationBuilder().token(tg_bot_token).build()

    start_handler = CommandHandler("start", start)
    chat_handler = CommandHandler("chat", chat)
    application.add_handler(start_handler)
    application.add_handler(chat_handler)

    application.run_polling()


main()
