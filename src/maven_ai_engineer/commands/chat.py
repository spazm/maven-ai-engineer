import logging

from telegram import Update
from telegram.ext import ContextTypes

from maven_ai_engineer.openai import openai

logger = logging.getLogger(__name__)

messages = [
    {"role": "system", "content": "You are a helpful assistant that answers questions."}
]


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages.append({"role": "user", "content": update.message.text})
    completion = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    completion_answer = completion.choices[0].message
    messages.append(completion_answer)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=completion_answer.content
    )
