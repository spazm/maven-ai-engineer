import os

import pandas as pd

# import tiktoken
from dotenv import load_dotenv

# from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()  # take environment variables from .env.

# from .commands import openai  # noqa

DOMAIN = "developer.mozilla.org"


def remove_newlines(series):
    series = series.str.replace("\n", " ")
    series = series.str.replace("\\n", " ")
    series = series.str.replace("  ", " ")
    series = series.str.replace("  ", " ")
    return series


# Create a list to store the text files


def load_texts(domain=DOMAIN):
    texts = []
    # Get all the text files in the text directory
    for file in os.listdir("text/" + domain + "/"):
        # Open the file and read the text
        with open("text/" + domain + "/" + file, "r", encoding="UTF-8") as f:
            text = f.read()
            # we replace the last 4 characters to get rid of .txt, and replace _ with / to generate the URLs we scraped
            filename = file[:-4].replace("_", "/")
            """
            There are a lot of contributor.txt files that got included in the scrape, this weeds them out. There are also a lot of auth required urls that have been scraped to weed out as well
            """
            if filename.endswith(".txt") or "users/fxa/login" in filename:
                continue

            # then we replace underscores with / to get the actual links so we can cite contributions
            texts.append((filename, text))
    return texts


texts = load_texts(DOMAIN)
# Create a dataframe from the list of texts
df = pd.DataFrame(texts, columns=["fname", "text"])

# Set the text column to be the raw text with the newlines removed
df["text"] = df.fname + ". " + remove_newlines(df.text)
df.to_csv("processed/scraped.csv")
