import logging
import os

from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

load_dotenv()

tg_bot_token = os.getenv("TG_BOT_TOKEN")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    logging.info("Importing commands")
    from .commands import (
        chat,
        mozilla,
        reset,
        start,
        transcribe_message,
        voice_choice_callback,
    )

    logging.info("Building application")
    application = ApplicationBuilder().token(tg_bot_token).build()

    start_handler = CommandHandler("start", start)
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)
    mozilla_handler = CommandHandler("mozilla", mozilla)
    logging.info("Adding handlers")
    application.add_handler(start_handler)
    application.add_handler(chat_handler)
    application.add_handler(mozilla_handler)
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(MessageHandler(filters.VOICE, transcribe_message))
    application.add_handler(CallbackQueryHandler(voice_choice_callback))

    logging.info("polling")
    application.run_polling()


main()
