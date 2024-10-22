import os

import pandas as pd
import tiktoken
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI

load_dotenv()  # take environment variables from .env.

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DOMAIN = "developer.mozilla.org"


def remove_newlines(series):
    series = series.str.replace("\n", " ")
    series = series.str.replace("\\n", " ")
    series = series.str.replace("  ", " ")
    series = series.str.replace("  ", " ")
    return series
