import logging
import json

from maven_ai_engineer.openai import openai
from telegram import Update
from telegram.ext import ContextTypes

from ..functions import functions, run_function
from ..prompts import CODE_PROMPT

logger = logging.getLogger(__name__)

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that answers questions.",
    },
    {"role": "system", "content": CODE_PROMPT},
]


def _chat(content):
    messages.append({"role": "user", "content": content})
    completion = openai.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=functions
    )
    response = completion.choices[0].message
    messages.append(response)
    return response


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received chat request:%s", update.message.text)
    initial_response = _chat(update.message.text)
    final_response = None
    tool_calls = initial_response.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            response = run_function(name, args)
            logger.info("tool_calls: %s", tool_calls)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": name,
                    "content": str(response),
                }
            )
            if name == "svg_to_png_bytes":
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id, photo=response
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "system",
                        "name": name,
                        "content": "Image was sent to the user, do not send the base64 string to them.",
                    }
                )
            # Generate the final response
            final_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            final_answer = final_response.choices[0].message

            # Send the final response if it exists
            if final_answer:
                messages.append(final_answer)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=final_answer.content
                )
            else:
                # Send an error message if something went wrong
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="something wrong happened, please try again",
                )

    else:
        # no tool call
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=initial_response.content
        )
