
# services/rag/query_preprocessor.py

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("API_KEY_OpenAI"))

def rewrite_query(query: str) -> str:
    """Fix grammar and simplify the original query"""
    prompt = (
        f"Rewrite the following question to fix grammar, clarify meaning, and make it concise:\n\n"
        f"Original: {query}\n\nRewritten:"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def expand_query(query: str, n_variants: int = 3) -> list[str]:
    """Generate alternative query phrasings (synonyms, rephrasing)"""
    prompt = (
        f"Generate {n_variants} different ways to ask the following question, "
        f"using synonyms or different phrasing. Include common abbreviations if helpful.\n\n"
        f"Question: {query}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return [
        line.strip("- ").strip()
        for line in response.choices[0].message.content.strip().split("\n")
        if line.strip()
    ]
