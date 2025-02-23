import os
import chromadb
from chromadb.utils import embedding_functions
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

class RAGSystem:
    def __init__(self, collection_name):
        """
        Initialize the RAG system with a collection name and OpenAI API key.

        :param collection_name: Name of the collection in ChromaDB.
        :param openai_api_key: OpenAI API key for embeddings and generation.
        :param chroma_db_path: Path to store ChromaDB data (default: "chroma_db").
        """
        self.collection_name = collection_name
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = chromadb.HttpClient(
                host=setting_core.CHROMA_SERVER_HOST,
                port=setting_core.CHROMA_SERVER_PORT,
                settings=Settings(allow_reset=True, anonymized_telemetry=False)
            )

        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)


        
        # Create or load the collection
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def load_and_split_document(self, file_path):
        """
        Load and split the document into chunks.

        :param file_path: Full path to the document file.
        :return: List of document chunks.
        """
        loader = TextLoader(file_path)
        documents = loader.load()

        # Split the document into smaller chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        return texts

    def create_embeddings_and_store(self, file_path):
        """
        Create embeddings for the document and store them in ChromaDB.

        :param file_path: Full path to the document file.
        """
        texts = self.load_and_split_document(file_path)

        # Create embeddings and store in ChromaDB
        for i, text in enumerate(texts):
            embedding = self.embeddings.embed_query(text.page_content)
            self.collection.add(
                ids=[str(i)],
                embeddings=[embedding],
                documents=[text.page_content]
            )

    def query(self, question):
        """
        Query the RAG system with a question.

        :param question: The question to ask.
        :return: The generated response.
        """
        # Retrieve relevant documents from ChromaDB
        results = self.collection.query(
            query_embeddings=[self.embeddings.embed_query(question)],
            n_results=5
        )

        # Combine retrieved documents into a single context
        context = "\n".join(results['documents'][0])

        # Use OpenAI to generate a response
        llm = OpenAI(openai_api_key=self.openai_api_key)
        response = llm.generate(prompt=f"Context: {context}\n\nQuestion: {question}\n\nAnswer:")

        return response.generations[0].text

# Example usage
'''
if __name__ == "__main__":
    # Initialize the RAG system
    rag = RAGSystem(collection_name="my_collection")

    # Load a document and create embeddings
    rag.create_embeddings_and_store("/path/to/your/document.txt")

    # Query the RAG system
    question = "What is the main topic of the document?"
    answer = rag.query(question)
    print("Answer:", answer)
    '''