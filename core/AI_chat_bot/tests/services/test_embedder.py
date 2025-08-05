from django.test import TestCase
import os
from AI_chat_bot.services.embedder import embed_texts

# AI_chat_bot/tests/services/rag/test_embedder.py


class OpenAIEmbedderIntegrationTest(TestCase):
    def setUp(self):
        # Ensure API key is present
        self.api_key = os.getenv("API_KEY_OpenAI")
        if not self.api_key:
            self.skipTest("OPENAI_API_KEY not set. Skipping real API test.")

    def test_embed_texts_with_real_openai_api(self):
        # Given
        input_texts = ["This is a test sentence.", "Another short example."]

        # When
        result = embed_texts(input_texts)

        # Then
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(vec, list) for vec in result))
        self.assertTrue(all(isinstance(num, float) for num in result[0]))
        self.assertGreater(len(result[0]), 100)  # Typical embedding size: 1536+
