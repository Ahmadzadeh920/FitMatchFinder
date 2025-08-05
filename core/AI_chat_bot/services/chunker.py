#Document chunking & optional embedding (used during indexing)
# services/rag/chunker.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

# Returns a single string with all pages concatenated, separated by newlines
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

# Raw string text (from PDF or other source)

def chunk_text(text, chunk_size=256, chunk_overlap=30):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)
