import os
from colivara_py import ColiVara
from pathlib import Path
import base64
from openai import OpenAI


class ColivaraRAG:
    def __init__(self, collection_name):
        """
        Initialize the RAG system with a collection name and OpenAI API key.

        :param collection_name: Name of the collection in ChromaDB.
        :param openai_api_key: OpenAI API key for embeddings and generation.
        :param chroma_db_path: Path to store ChromaDB data (default: "chroma_db").
        """
        self.collection_name = collection_name
        self.openai_api_key = os.getenv("API_KEY_OpenAI")
        self.colivera_api_key = os.getenv("API_KEY_COLIVARA")
        
        # Initialize OpenAI embeddings
        self.llm_client = OpenAI(api_key=self.openai_api_key)
        self.rag_client = ColiVara(
            base_url="https://api.colivara.com", 
            api_key=self.colivera_api_key
        )

    def sync_document(self, file_path, id_file):
        """Sync a single document to the ColiVara server."""
        file = Path(file_path)
        
        if not file.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        # manage collection
        try:
        # Try to get the existing collection
            self.collection = self.rag_client.get_collection(collection_name=self.collection_name)
        except:  # Collection doesn't exist
    # Create a new collection with metadata
            self.collection = self.rag_client.create_collection(
            name=self.collection_name,
           
            )
       
        with open(file, 'rb') as f:
            file_content = f.read()
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            document_out = self.rag_client.upsert_document(
                name=str(id_file), 
                document_base64=encoded_content,
                #document_url=file_path, 
                collection_name=self.collection_name, 
                wait=True
            )
            return document_out
        return False
    



    def delete_document(self, id_file):
        """Delete a document from the ColiVara server."""
        try:
        # Try to get the existing collection
            self.collection = self.rag_client.get_collection(collection_name=self.collection_name)

        except ValueError:  # Collection doesn't exist
            raise ValueError(f"Collection {self.collection_name} does not exist.")
        # Delete the document from the collection
        try :
            self.rag_client.get_document(document_name=str(id_file), collection_name=self.collection_name)
            self.rag_client.delete_document(
                document_name=str(id_file), 
                collection_name=self.collection_name
            )
            return True
        except ValueError:
            raise ValueError(f"Document {id_file} does not exist in collection {self.collection_name}.")


    def transform_query(self, messages):
        prompt = """ 
        You are given a conversation between a user and an assistant. We need to transform the last message from the user into a question appropriate for a RAG pipeline.
        Given the nature and flow of conversation. 

        Example #1:
        User: What is the capital of Brazil?
        Assistant: Brasília
        User: How about France?
        RAG Query: What is the capital of France?
        <reasoning> 
        Somewhat related query, however, if we simply use "how about france?" without any transformation, the RAG pipeline will not be able to provide a meaningful response.
        The transformation took the previous question (what the capital of Brazil?) as a strong hint about the user intention
        </reasoning>

        Example #2:
        User: What is the policy on working from home? 
        Assistant: <policy details>
        User: What is the side effects of Wegovy?
        RAG Query: What are the side effects of Wegovy?
        <reasoning>
        The user is asking for the side effects of Wegovy, the transformation is straightforward, we just need to slightly adjust. 
        The previous question was about a completely different topic, so it has no influence on the transformation.
        </reasoning>

        Example #3:
        User: What is the highest monetary value of a gift I can recieve from a client?
        Assistant: <policy details>
        User: Is there a time limit between gifts?
        RAG Query: What is the highest monetary value of a gift I can recieve from a client within a specific time frame?
        <reasoning>
        The user queries are very related and a continuation of the same question. He is asking for more details about the same topic.
        The transformation needs to take into account the previous question and the current one.
        </reasoning>

        Example #4:
        User: Hello!
        RAQ Query: Not applicable
        <reasoning>
        The user is simply greeting the assistant, there is no question to transform. This applies to any non-question message,
        </reasoning>

        Coversation:
        """
        for message in messages:
            prompt += f"{message['role']}: {message['content']}\n"

        response = self.llm_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "assistant", "content": prompt}],
            stream=False,
        )
        query = response.choices[0].message.content
        return query

    def run_rag_pipeline(self, query):
        # clean the query that came from the LLM
        if "not applicable" in query.lower():
            # don't need to run RAG or get a context
            return []
        if "rag query:" in query.lower():
            query = query.split("ry:")[1].strip()
        
        if "<reasoning>" in query:
            query = query.split("<reasoning>")[0].strip()

        print(f"This what we will send to the RAG pipeline: {query}")
        results = self.rag_client.search(query=query, 
                                         collection_name=self.collection_name,
                                           top_k=5,
                                            
    
         
                                      )
        
        
        print("collection name: ", self.collection_name)
        results = results.results
        context = []
        for result in results:
            document_title = result.document_name
            page_num = result.page_number
            base64 = result.img_base64
             # base64 doesn't have data: part so we need to add it
            if "data:image" not in base64:
                base64 = f"data:image/png;base64,{base64}"
            context.append(
                {
                    "metadata": f"{document_title} - Page {page_num}",
                    "base64": base64,
                }
            )
        return context

    

    def draft_response(self, messages):
        query = self.transform_query(messages) 
        context = self.run_rag_pipeline(query)
        
        return  context
    

    def create_collection_document_map(self):
        """
        Creates a dictionary mapping collection names to sets of their document names.
        
        Returns:
            dict: A dictionary where keys are collection names and values are sets of document names.
        """
    
        collection_doc_map = {}
        collections = self.rag_client.list_collections()
    
        for collection in collections:
            try:
                documents = self.rag_client.list_documents(
                    collection_name= collection.name,
                   
            )
            
            # Convert to list immediately instead of set
                document_names = [doc.name for doc in documents]  # Changed to list comprehension
                collection_doc_map[collection.name] = document_names  # Store as list instead of set
            
            except Exception as e:
                print(f"Error processing collection {collection.name}: {str(e)}")
                collection_doc_map[collection.name] = []  # Empty list instead of set
        
        return collection_doc_map