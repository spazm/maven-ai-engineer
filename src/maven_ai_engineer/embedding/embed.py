import logging
import os
from pathlib import Path

import pandas as pd
import tiktoken
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()  # take environment variables from .env.

from maven_ai_engineer.openai import openai  # noqa

DOMAIN = "developer.mozilla.org"
ROOT_PATH = Path(__file__).parent.parent

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def remove_newlines(series):
    series = series.str.replace("\n", " ")
    series = series.str.replace("\\n", " ")
    series = series.str.replace("  ", " ")
    series = series.str.replace("  ", " ")
    return series


def load_texts(domain=DOMAIN):
    texts = []
    text_path = ROOT_PATH / "text"

    # Get all the text files in the text directory
    for file in os.listdir(text_path / domain):
        logging.info(f"loading text: {file}")
        # Open the file and read the text
        with open(text_path / domain / file, "r", encoding="UTF-8") as f:
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


def process_scraped():
    logger.info("Processing scraped texts")
    texts = load_texts(DOMAIN)
    # Create a dataframe from the list of texts
    logger.info("Converting to dataframe")
    df = pd.DataFrame(texts, columns=["fname", "text"])

    # Set the text column to be the raw text with the newlines removed
    logger.info("Removing newlines")
    df["text"] = df.fname + ". " + remove_newlines(df.text)
    logger.info("Writing scraped.csv")
    df.to_csv(ROOT_PATH / "processed" / "scraped.csv")
    logger.info("Done Processing scraped texts")


# Load the cl100k_base tokenizer which is designed to work with the ada-002
# model
tokenizer = tiktoken.get_encoding("cl100k_base")


def process_embeddings():
    """
    chunk and create embeddings for texts from scraped.csv
    """
    logger.info("Processing embeddings")

    logger.info("read scraped.csv")
    df = pd.read_csv(ROOT_PATH / "processed" / "scraped.csv", index_col=0)
    df.columns = ["title", "text"]

    # Tokenize the text and save the number of tokens to a new column
    logger.info("Applying tokenizer")
    df["n_tokens"] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    chunk_size = 1000  # Max number of tokens

    logger.info("Splitting long text")
    text_splitter = RecursiveCharacterTextSplitter(
        # This could be replaced with a token counting function if needed
        length_function=len,
        chunk_size=chunk_size,
        chunk_overlap=0,  # No overlap between chunks
        add_start_index=False,  # We don't need start index in this case
    )

    shortened = []

    for row in df.iterrows():

        # If the text is None, go to the next row
        if row[1]["text"] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]["n_tokens"] > chunk_size:
            # Split the text using LangChain's text splitter
            chunks = text_splitter.create_documents([row[1]["text"]])
            # Append the content of each chunk to the 'shortened' list
            for chunk in chunks:
                shortened.append(chunk.page_content)

        # Otherwise, add the text to the list of shortened texts
        else:
            shortened.append(row[1]["text"])

    df = pd.DataFrame(shortened, columns=["text"])
    logger.info("Applying tokenizer on shortened")
    df["n_tokens"] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    logger.info("creating embeddings")
    df["embeddings"] = df.text.apply(
        lambda x: openai.embeddings.create(input=x, model="text-embedding-ada-002")
        .data[0]
        .embedding
    )

    logger.info("writing embeddings.csv")
    df.to_csv(ROOT_PATH / "processed" / "embeddings.csv")
    logger.info("done with embeddings")


if __name__ == "__main__":
    process_scraped()
    # process_embeddings()
