# LLM-Based Re-ranking

# services/rag/reranker.py

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("API_KEY_OpenAI"))

def rerank_chunks(query: str, chunks: list[str]) -> list[str]:
    prompt = (
        f"Given the following question:\n"
        f"{query}\n\n"
        f"Rank the following text chunks by their relevance to the question. "
        f"Return them in descending order of importance. Keep only the top ones.\n\n"
    )

    for i, chunk in enumerate(chunks):
        prompt += f"Chunk {i+1}:\n{chunk}\n\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    # Very basic: just return chunks as-is assuming original order
    # You can parse returned text if you want strict ordering
    return chunks  # or re-ordered list parsed from `response`
