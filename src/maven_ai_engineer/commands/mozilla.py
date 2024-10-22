import logging
from pathlib import Path

import numpy as np
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

from ..questions import answer_question

logger = logging.getLogger(__name__)

# Get the directory of the current script
ROOT_PATH = Path(__file__).parent.parent

# Construct the absolute path to the CSV file
csv_path = ROOT_PATH / "processed" / "embeddings.csv"
df = pd.read_csv(csv_path, index_col=0)
df["embeddings"] = df["embeddings"].apply(eval).apply(np.array)


async def mozilla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = answer_question(df, question=update.message.text, debug=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
