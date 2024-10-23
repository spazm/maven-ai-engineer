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
    logging.info("Importing commands")
    from .commands import chat, mozilla, start

    logging.info("Building application")
    application = ApplicationBuilder().token(tg_bot_token).build()

    start_handler = CommandHandler("start", start)
    chat_handler = CommandHandler("chat", chat)
    mozilla_handler = CommandHandler("mozilla", mozilla)
    logging.info("Adding handlers")
    application.add_handler(start_handler)
    application.add_handler(chat_handler)
    application.add_handler(mozilla_handler)

    logging.info("polling")
    application.run_polling()


main()
