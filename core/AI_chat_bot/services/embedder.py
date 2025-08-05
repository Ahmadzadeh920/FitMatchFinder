#Text to vector conversion using an embedding modelimport openai
# services/rag/embedder.py

from openai import OpenAI
import os

openai_client = OpenAI(api_key=os.getenv("API_KEY_OpenAI"))

def embed_texts(texts: list[str]) -> list[list[float]]:
    response = openai_client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    return [record.embedding for record in response.data]
