# AI_chat_bot/tests/services/rag/test_retriever.py

import os
from django.test import TestCase
from AI_chat_bot.services import retriever
import time

class PineconeRetrieverIntegrationTest(TestCase):
    def setUp(self):
        self.api_key = "test_pinecone_rag"
        self.index_name = retriever.get_index_name(self.api_key)
        self.index = retriever.get_or_create_index(self.index_name)

        self.texts = [
            "This is the first test chunk.",
            "Second test paragraph with different content.",
        ]
        self.embeddings = [
            [0.1] * 1536,
            [0.1] * 1536
        ]
        self.metadatas = [
            {"page": 1, "source": "test1"},
            {"page": 2, "source": "test2"}
        ]

        # Ensure a clean test index (by recreating it)
        if self.index_name in retriever.pc.list_indexes().names():
            retriever.pc.delete_index(self.index_name)
        self.index = retriever.get_or_create_index(self.index_name)

    def test_store_embeddings_creates_vectors(self):
        retriever.store_embeddings(
            index=self.index,
            texts=self.texts,
            embeddings=self.embeddings,
            metadatas=self.metadatas
        )

        time.sleep(3)  # Let Pinecone finish indexing

        query_embedding = [0.1] * 1536
        result = self.index.query(vector=query_embedding, top_k=2, include_metadata=True)

        print("Query matches:", result.matches)

        self.assertGreaterEqual(len(result.matches), 1, "Expected at least 1 match")
        texts = [m.metadata.get("text") for m in result.matches]
        self.assertIn("This is the first test chunk.", texts)

    def test_retrieve_similar_chunks_returns_expected_result(self):
        retriever.store_embeddings(
            index=self.index,
            texts=self.texts,
            embeddings=self.embeddings,
            metadatas=self.metadatas
        )

        query_embedding = [0.2] * 1536
        result = retriever.retrieve_similar_chunks(self.index, query_embedding, top_k=1)

        self.assertIn("documents", result)
        self.assertEqual(len(result["documents"][0]), 1)
        self.assertEqual(result["documents"][0][0], "Second test paragraph with different content.")
        self.assertEqual(result["metadatas"][0][0]["page"], 2)

    def tearDown(self):
        # Delete test index to keep Pinecone clean
        retriever.pc.delete_index(self.index_name)
