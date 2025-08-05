from django.test import TestCase
from AI_chat_bot.services import query_preprocessor



class QueryPreprocessorTest(TestCase):
    def test_rewrite_query_simplifies_text(self):
        raw_query = "  What IS   the ReturN policy?  "
        rewritten = query_preprocessor.rewrite_query(raw_query)

        self.assertIsInstance(rewritten, str)
        self.assertEqual(rewritten.lower(), "what is the return policy?")

    def test_expand_query_returns_multiple_variations(self):
        base_query = "return policy"
        expanded = query_preprocessor.expand_query(base_query)

        self.assertIsInstance(expanded, list)
        self.assertGreaterEqual(len(expanded), 2)
        
        self.assertTrue(
            any("return policy" in q.lower() for q in expanded),
            "Expected 'return policy' in at least one query expansion"
        )


    def test_expand_query_does_not_return_duplicates(self):
        base_query = "cancel order"
        expanded = query_preprocessor.expand_query(base_query)

        self.assertEqual(len(expanded), len(set(expanded)), "Query expansion should not include duplicates")

    def test_empty_query_returns_fallback(self):
        empty_query = ""
        rewritten = query_preprocessor.rewrite_query(empty_query)
        expanded = query_preprocessor.expand_query(empty_query)

        self.assertTrue(len(rewritten) > 0, "Expected a non-empty fallback from OpenAI for empty input.")
        self.assertIsInstance(expanded, list)
        self.assertGreaterEqual(len(expanded), 1)
