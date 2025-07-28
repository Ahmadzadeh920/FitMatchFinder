#Document chunking & optional embedding (used during indexing)
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_document(text, chunk_size=256, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)
