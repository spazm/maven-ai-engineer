from telegram import Update
from telegram.ext import ContextTypes

from .chat import chat
from .mozilla import mozilla


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


__all__ = [start, chat, mozilla]
