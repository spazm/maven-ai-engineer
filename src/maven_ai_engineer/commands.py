import logging
import os

from openai import OpenAI
from telegram import Update
from telegram.ext import ContextTypes

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

logger = logging.getLogger(__name__)

messages = [
    {"role": "system", "content": "You are a helpful assistant that answers questions."}
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages.append({"role": "user", "content": update.message.text})
    completion = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    completion_answer = completion.choices[0].message
    messages.append(completion_answer)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=completion_answer.content
    )
