#Controls: Entire RAG flow (Orchestration Layer)



from AI_chat_bot.services.chunker import extract_text_from_pdf, chunk_text
from AI_chat_bot.services.embedder import embed_texts
from AI_chat_bot.services.query_preprocessor import rewrite_query, expand_query
from services.rag.retriever import get_index_name,get_or_create_index,store_embeddings,retrieve_similar_chunks
from AI_chat_bot.services.reranker import rerank_chunks
from AI_chat_bot.services.compressor import compress_context
from AI_chat_bot.models import Reference

class RAG:
    def __init__(self, api_key):
        self.api_key = str(api_key)
        self.index_name = get_index_name(self.api_key)
        self.index = get_or_create_index(self.index_name)

    def index_documents(self):
        references = Reference.objects.filter(API_Key__api_key=self.api_key)
        for ref in references:
            path = ref.reference_doc.path
            text = extract_text_from_pdf(path)
            chunks = chunk_text(text)
            embeddings = embed_texts(chunks)
            store_embeddings(self.index, chunks, embeddings)

    def retrieve_context(self, original_question: str, top_k: int = 5):
        # Query Preprocessing
        rewritten = rewrite_query(original_question)
        variations = [rewritten] + expand_query(rewritten)

        # Retrieval
        all_chunks = []
        seen_ids = set()
        for var in variations:
            embedding = embed_texts([var])[0]
            results = retrieve_similar_chunks(self.index, embedding)
            for doc, meta, id_ in zip(results['documents'][0], results['metadatas'][0], results['ids'][0]):
                if id_ not in seen_ids:
                    all_chunks.append(doc)
                    seen_ids.add(id_)

        # Post-Retrieval: Re-ranking
        ranked_chunks = rerank_chunks(original_question, all_chunks)

        # Post-Retrieval: Context Compression
        compressed_context = compress_context(ranked_chunks, original_question)

        return compressed_context

    def answer(self, question: str):
        context = self.retrieve_context(question)
        prompt = (
            f"Answer the question based only on the context below.\n\n"
            f"Context:\n{''.join(context)}\n\n"
            f"Question: {question}"
        )
        # You can use OpenAI or any LLM here
        return self._call_llm(prompt)

    def _call_llm(self, prompt: str) -> str:
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",  # or gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
