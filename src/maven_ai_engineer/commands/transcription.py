from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from maven_ai_engineer.openai import openai


async def transcribe_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Make sure we have a voice file to transcribe
    voice_id = update.message.voice.file_id
    if voice_id:
        file = await context.bot.get_file(voice_id)
        await file.download_to_drive(f"voice_note_{voice_id}.ogg")
        await update.message.reply_text("Voice note downloaded, transcribing now")
        audio_file = open(f"voice_note_{voice_id}.ogg", "rb")
        transcript = openai.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
        await update.message.reply_text(f"Transcript finished:\n {transcript.text}")

        # Save the transcribed text to context for later use
        context.user_data["transcribed_text"] = transcript.text
        context.user_data["voice_id"] = voice_id

        keyboard = [
            [InlineKeyboardButton("Alloy", callback_data="alloy")],
            [InlineKeyboardButton("Echo", callback_data="echo")],
            [InlineKeyboardButton("Fable", callback_data="fable")],
            [InlineKeyboardButton("Onyx", callback_data="onyx")],
            [InlineKeyboardButton("Nova", callback_data="nova")],
            [InlineKeyboardButton("Shimmer", callback_data="shimmer")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Please choose a voice for the TTS:", reply_markup=reply_markup
        )


async def voice_choice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Get the user's selected voice
    selected_voice = query.data
    transcribed_text = context.user_data.get("transcribed_text")
    voice_id = context.user_data.get("voice_id")

    if transcribed_text and selected_voice:
        await query.edit_message_text(
            f"You chose {selected_voice}. Generating the voice note..."
        )

        # Generate a new voice note using the selected TTS voice
        tts_response = openai.audio.speech.create(
            model="tts-1", voice=selected_voice, input=transcribed_text
        )

        # Save the TTS response to a file
        tts_voice_note_path = f"tts_voice_note_{voice_id}.mp3"
        tts_response.stream_to_file(tts_voice_note_path)

        # Send the TTS-generated voice note back to the user
        with open(tts_voice_note_path, "rb") as tts_voice_note:
            await context.bot.send_voice(
                chat_id=query.message.chat_id,
                voice=tts_voice_note,
                caption=f"Here is the TTS version of your message in the {selected_voice.capitalize()} voice.",
            )
