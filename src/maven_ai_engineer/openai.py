import os

from openai import OpenAI

openai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
