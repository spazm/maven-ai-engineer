import logging

from telegram import Update
from telegram.ext import ContextTypes

from maven_ai_engineer.openai import openai

logger = logging.getLogger(__name__)

messages = [
    {"role": "system", "content": "You are a helpful assistant that answers questions."}
]


def _chat(content):
    messages.append({"role": "user", "content": content})
    completion = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    completion_answer = completion.choices[0].message
    messages.append(completion_answer)
    return completion_answer.content

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received chat request:%s", update.message.text)
    completion_answer_content = _chat(update.message.text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=completion_answer_content
    )
