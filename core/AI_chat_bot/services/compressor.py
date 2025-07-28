# services/rag/compressor.py
'''
What it does: After re-ranking, reduces chunk size via:

        Summarization

        Trimming redundant phrases

        Filtering off-topic sentences
        
'''
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("API_KEY_OpenAI"))

def compress_context(chunks: list[str], query: str, max_tokens=1024) -> str:
    """Summarize or trim chunks to make space in LLM prompt"""
    joined = "\n\n".join(chunks)
    prompt = (
        f"The following text chunks were retrieved in response to the question:\n"
        f"{query}\n\n"
        f"Please compress the context below to remove redundancy and off-topic info, keeping max {max_tokens} tokens.\n\n"
        f"{joined}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
