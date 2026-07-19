"""
rag_utils.py
Shared helper functions used by both ingest.py and app.py.
This file does the "behind the scenes" work: reading PDFs, splitting text
into chunks, turning text into embeddings, and talking to ChromaDB.
"""

import os
from google import genai
from google.genai import types
from pypdf import PdfReader
import chromadb
from dotenv import load_dotenv

# Load the GEMINI_API_KEY from the .env file into the environment
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model names — if one stops working, check https://ai.google.dev/gemini-api/docs/models
EMBEDDING_MODEL = "gemini-embedding-001"
GENERATION_MODEL = "gemini-2.0-flash"

CHROMA_DB_PATH = "./chroma_db"   # folder where the vector database is saved on disk
COLLECTION_NAME = "documents"     # name of our collection inside ChromaDB


def get_client():
    """Create and return a Gemini API client using the key from .env"""
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not found. Make sure you created a .env file "
            "with your API key inside it."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def extract_text_from_pdf(pdf_path):
    """Reads a PDF file and returns all its text as one big string."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits a long piece of text into smaller overlapping chunks.
    chunk_size = how many words per chunk
    overlap = how many words repeat between one chunk and the next
              (this helps preserve context across chunk boundaries)
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def embed_texts(client, texts, task_type="RETRIEVAL_DOCUMENT"):
    """
    Converts a list of text strings into embedding vectors using Gemini.
    task_type should be:
      - "RETRIEVAL_DOCUMENT" when embedding chunks you're storing
      - "RETRIEVAL_QUERY"    when embedding a user's question
    """
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(task_type=task_type),
    )
    return [emb.values for emb in result.embeddings]


def get_collection():
    """Opens (or creates, if it doesn't exist yet) our ChromaDB collection."""
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
    return collection
