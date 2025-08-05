import os
from pinecone import Pinecone, ServerlessSpec
from typing import List

# Load credentials from env
PINECONE_API_KEY = os.getenv("API_KEY_PINECONE")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")  # or your chosen region
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")          # aws | gcp | azure

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define tenant-to-index mapping
INDEX_NAME_PREFIX = "rag"

import re

def get_index_name(api_key: str) -> str:
    # Replace any invalid characters with hyphens
    safe_key = re.sub(r'[^a-z0-9-]', '-', api_key.lower())
    return f"{INDEX_NAME_PREFIX}-{safe_key}"


def get_or_create_index(index_name: str, dimension: int = 1536):
    if index_name not in pc.list_indexes().names():
        pc.create_index_for_model(
            name=index_name,
            model="text-embedding-3-small",
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-west-2")
        )

    return pc.Index(index_name)

def store_embeddings(index, texts: List[str], embeddings: List[List[float]], metadatas: List[dict] = None):
    vectors = []
    for i, embedding in enumerate(embeddings):
        metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
        metadata["text"] = texts[i]  # store original text
        vectors.append((f"chunk-{i}", embedding, metadata))
    
    index.upsert(vectors=vectors)

def retrieve_similar_chunks(index, query_embedding: List[float], top_k: int = 5):
    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    documents = [match.metadata.get("text", "") for match in result.matches]
    metadatas = [match.metadata for match in result.matches]
    ids = [match.id for match in result.matches]

    return {
        "documents": [documents],  # match ChromaDB format
        "metadatas": [metadatas],
        "ids": [ids]
    }
