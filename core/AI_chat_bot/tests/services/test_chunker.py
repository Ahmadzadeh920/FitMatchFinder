# AI_chat_bot/tests/test_chunker.py

import os
import tempfile
from django.test import TestCase
from AI_chat_bot.services.chunker import extract_text_from_pdf, chunk_text
from PyPDF2 import PdfWriter

class TestChunker(TestCase):

    def create_sample_pdf(self, content="Hello world. This is a test PDF."):
        pdf_writer = PdfWriter()
        pdf_writer.add_blank_page(width=72, height=72)
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        with open(temp_pdf.name, "wb") as f:
            pdf_writer.write(f)
        return temp_pdf.name

    def test_chunk_text_basic(self):
        text = "This is sentence one. This is sentence two. This is sentence three."
        chunks = chunk_text(text, chunk_size=20, chunk_overlap=5)
        self.assertIsInstance(chunks, list)
        self.assertTrue(all(isinstance(c, str) for c in chunks))
        self.assertGreaterEqual(len(chunks), 1)

    def test_chunk_text_overlap(self):
        text = "A" * 1000
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)
        self.assertTrue(all(len(c) <= 100 for c in chunks))
        self.assertGreater(len(chunks), 1)

    def test_extract_text_from_pdf_empty_page(self):
        pdf_path = self.create_sample_pdf()
        result = extract_text_from_pdf(pdf_path)
        self.assertIsInstance(result, str)
        self.assertEqual(result.strip(), "")
        os.remove(pdf_path)

    
