# 🧠 RAG Engine - SaaS Chatbot Module

This module implements a **Retrieval-Augmented Generation (RAG)** system tailored for a **SaaS platform** where each tenant (e.g., online shop) has its own isolated knowledge base, identified by a unique `API_Key`.

It leverages **OpenAI**, **ChromaDB**, and **Langchain** to enable intelligent, context-aware responses from your clients’ uploaded documents.



## 📁 Folder Structure
    ├── __init__.py                    # Makes this a Python module
    ├── rag_engine.py                 # 🚀 Main RAG class that ties all components together

    ├── chunker.py                    # 📄 Extracts and chunks document text (e.g., from PDFs)
    ├── embedder.py                   # 🔢 Generates embeddings using OpenAI's text-embedding-3-small
    ├── retriever.py                  # 🧠 Handles storing and retrieving from ChromaDB (per API_Key)

    ├── query_preprocessor.py         # 🔍 Rewrites and expands user queries before retrieval
    ├── reranker.py                   # 🎯 Reorders retrieved chunks based on relevance to the query
    ├── compressor.py                 # ✂️ Compresses context to avoid token overflow and reduce redundancy

    └── README.md                     # 📘 Documentation for the RAG module (you just created this)





## 🏗️ RAG Pipeline Overview

The RAG pipeline handles document ingestion, query understanding, context retrieval, and final LLM-based response generation.

### 📄 1. Document Preprocessing

- **Chunking**: Documents are split using fixed-size token chunks (default: 256), optionally with overlap.
  - Tool: [`langchain.text_splitter`](https://docs.langchain.com/docs/modules/data_connection/document_transformers/text_splitters)
- **Embedding**: Chunks are encoded into vectors using [`text-embedding-3-small`](https://platform.openai.com/docs/guides/embeddings) from OpenAI.
- **Storage**: Embeddings are stored in [`ChromaDB`](https://docs.trychroma.com/) with collection names matching each `API_Key`.

---

### 🤖 2. Query Preprocessing

- **Query Rewriting**: Cleans the user input (e.g., grammar, clarity).
- **Query Expansion**: Generates semantically related variations using GPT-3.5.

---

### 🔍 3. Retrieval

- Each variation is embedded and used to retrieve top-k matching chunks from ChromaDB.
- Retrieved chunks are deduplicated before being passed to post-processing.

---

### 🧠 4. Post-Retrieval Optimization

- **Re-ranking**: Uses [`gpt-3.5-turbo`](https://platform.openai.com/docs/guides/chat) to reorder chunks based on relevance to the original query.
- **Context Compression**: Trims or summarizes long or low-value context to fit the LLM input window.

---

### 💬 5. Answer Generation

- The final prompt is composed using the user’s original question and optimized context.
- Answer is generated using `gpt-4` or `gpt-3.5-turbo`.

---




## 🛠 Dependencies

```bash
pip install openai langchain chromadb PyPDF2
```

## 🔐 Tenant Isolation
Each tenant (e.g., online shop) uses a unique API_Key.
All documents and vectors are stored in ChromaDB collections named after this API_Key.

## ✅ RAG Class Usage

```bash
from services.rag.rag_engine import RAG

rag = RAG(api_key="shop-1234")

# Step 1: Index PDFs for the tenant
rag.index_documents()

# Step 2: Ask a question
response = rag.answer("What is your return policy?")
print(response)


 ```



## 🔍 Model & Tools Choices
| Stage           | Tool/Model                      | Description                               |
| --------------- | ------------------------------- | ----------------------------------------- |
| Chunking        | Langchain                       | Token-based splitting with overlap        |
| Embedding       | OpenAI `text-embedding-3-small` | Lightweight, accurate, SaaS-compatible    |
| Retrieval       | ChromaDB                        | Local vector database, per-tenant storage |
| Query Expansion | GPT-3.5                         | Generates semantic variations             |
| Re-ranking      | GPT-3.5                         | Scores chunk relevance                    |
| Compression     | GPT-3.5                         | Summarizes and trims content              |
| LLM Response    | GPT-4 or GPT-3.5                | Generates final answer                    |



## 👩‍💻 Maintainers
Designed by: Fatemeh Ahmadzadeh

Maintained in: services


## 📚 References

Here are the main technologies, models, and libraries used in this RAG engine:

| Component               | Resource                                                                 |
|-------------------------|--------------------------------------------------------------------------|
| 🔗 OpenAI Embeddings    | [OpenAI Text Embedding Models](https://platform.openai.com/docs/guides/embeddings) |
| 🤖 GPT-3.5 / GPT-4       | [OpenAI Chat Completions API](https://platform.openai.com/docs/guides/chat)       |
| 🧱 ChromaDB             | [Chroma Vector Database](https://docs.trychroma.com/)                   |
| 🧠 Langchain            | [Langchain Text Splitters](https://docs.langchain.com/docs/modules/data_connection/document_transformers/text_splitters) |
| 📄 PyPDF2 (PDF parsing) | [PyPDF2 Documentation](https://pypdf2.readthedocs.io/en/latest/)         |
| 🧾 Retrieval-Augmented Generation | [Original RAG Paper (Facebook AI)](https://arxiv.org/abs/2005.11401)      |
| 🔬 SentenceTransformers (optional) | [SentenceTransformers Documentation](https://www.sbert.net/)                  |
| 🛠 Django               | [Django Project](https://www.djangoproject.com/)                         |

---

For deeper understanding of fine-tuning, query expansion, and hybrid search, you can also explore:

- [Fine-tuning OpenAI models](https://platform.openai.com/docs/guides/fine-tuning)
- [Langchain RAG Guide](https://docs.langchain.com/docs/use_cases/question_answering/how_to/rag)
- [Chroma Use Cases](https://docs.trychroma.com/usage-guide/)



## 📜 License
MIT License – free to use, modify, and build upon.


