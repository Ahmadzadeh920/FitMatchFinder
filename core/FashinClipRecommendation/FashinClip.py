from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel
import torch
import numpy as np
import chromadb
from chromadb.config import Settings
from django.conf import settings as setting_core

class FashionImageRecommender:
    def __init__(self, collection_name=None):
        self.model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
        self.processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")
        self.chroma_client = chromadb.HttpClient(
                host=setting_core.CHROMA_SERVER_HOST,
                port=setting_core.CHROMA_SERVER_PORT,
                settings=Settings(allow_reset=True, anonymized_telemetry=False)
            )
        self.collection_name= collection_name

    def load_images(self,full_image_path, id_img):

        """Loads images and creates embeddings."""

        image = Image.open(full_image_path).convert("RGB")
        embedding = self.create_embedding(image).tolist()
        print("embedding is " + str(embedding.shape))
        collection = self.chroma_client.get_or_create_collection(name=self.collection_name) 
        image_ids = [str(id_img)]
        try:
            collection.add(documents=[str(embedding)], ids=image_ids)  # Convert to a string representation
            return True
        except Exception as e:
            return False

    def create_embedding(self, image):
        """Generates an embedding for a given image."""
        # Preprocess the image as required by the model
        image = image.resize((224, 224))  #
        with torch.no_grad():
            inputs = self.processor(images=image, return_tensors="pt", padding=True)
            embedding = self.model.get_image_features(**inputs)
        return embedding.numpy()

    def Delete_embeded_images(self,id_img):
        collection = self.chroma_client.get_collection(name=self.collection_name) 
        image_ids = [str(id_img)]
       # Step 3: Delete the item
        try: 
            collection.delete(ids=image_ids)
            return True
        except Exception as e:
            print('error is'+ str(e))

# return the list includes all ids related to images in chromadb in the this collection
    def retrive_image(self):
        collection = self.chroma_client.get_collection(name=self.collection_name)
        documents = collection.get(include=["documents"])  # Call get_all directly on the collection object\ 
        ids_list= documents['ids']
        doc_list = documents['documents']
        num_rows = len(doc_list)  # Number of top-level elements
        num_cols = len(doc_list[0]) if num_rows > 0 else 0  # Length of the first nested list

        shape = (num_rows, num_cols)
        print("Shape of the list:", shape)
       
        
        return ids_list

# for consedering query in chromadb
    def query_collection(self, collection_name, query_texts, n_results=5):
        collection = self.get_or_create_collection(collection_name)
        return collection.query(query_texts=query_texts, n_results=n_results)


    def recommend_images(self, description, number_of_images=5):
        """Recommends images based on the user's description."""

        description_embedding = self.create_description_embedding(description)
        print("prompt is" + str(description_embedding.shape))
        description_embedding = description_embedding.tolist()
        collection = self.chroma_client.get_collection(self.collection_name)
        response= collection.get()
        embedding_imgs = response["documents"]
        ids_img = response["ids"]
        #result = collection.query(query_embeddings = description_embedding,n_results=2) 
       
        return response.keys()
        '''
        for i in range(number_of_images):
        similarities = collection.query(description_embedding)
        print(similarities)
        # Sort and get the top recommendations
        recommended_images = sorted(similarities, key=lambda x: x['similarity'], reverse=True)
        return recommended_images[:number_of_images]  # Return top 5 recommendations'''


    def create_description_embedding(self, description):
        """Generates an embedding for a given description."""
        try:
            self.chroma_client.get_collection(self.collection_name)
        except ValueError:
            return ("Collection does not exist")
        
        inputs_text = self.processor(text=description, return_tensors="pt", padding=True)
        with torch.no_grad():
            description_embedding = self.model.get_text_features(**inputs_text).numpy()

        return description_embedding


# Example usage
'''
    recommender = FashionImageRecommender(collection_name)

    # Load your images
    image_paths = ['path/to/image1.jpg', 'path/to/image2.jpg']
    recommender.load_images(image_paths)

    # Get recommendations based on user description
    user_description = "A red dress with floral patterns"
    recommendations = recommender.recommend_images(user_description, number_of_images = 10)
    '''