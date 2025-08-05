from PIL import Image
import requests
#from transformers import CLIPProcessor, CLIPModel
#import torch
import numpy as np
import chromadb
from chromadb.config import Settings


class FashionImageRecommender:
    def __init__(self, collection_name=None):
        self.model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
        self.processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")
        self.chroma_client = chromadb.HttpClient(
                    host=os.getenv("CHROMA_HOST", "chromadb"),
                    port=int(os.getenv("CHROMA_PORT", "8000")),
                    settings=Settings(allow_reset=True, anonymized_telemetry=False)
                )
        self.collection_name= collection_name

    def load_images(self,full_image_path, id_img):

        """Loads images and creates embeddings."""

        image = Image.open(full_image_path).convert("RGB")
        embedding = self.create_embedding(image).tolist()
        # Flatten the embedding to remove the extra dimension
        embedding = embedding[0]  # Extract the first (and only) row to make it a 1D list
        collection = self.chroma_client.get_or_create_collection(name=self.collection_name, metadata={"dimensionality": 512}) 
        image_ids = [str(id_img)]
        print('embedding is '+str(np.array(embedding).shape))
        try:
        # Add the embedding to the collection
            collection.add(
                embeddings=[embedding],  # Pass the embedding as a list of floats
                ids=image_ids  # Pass the ID as a list of strings
            )
            
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
        documents = collection.get(include=["embeddings"])  # Call get_all directly on the collection object\ 
        ids_list= documents['ids']
        doc_list = documents['embeddings']
        num_rows = len(doc_list)  # Number of top-level elements
        num_cols = len(doc_list[0]) if num_rows > 0 else 0  # Length of the first nested list

        shape = (num_rows, num_cols)
        
       
        
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
        
        result = collection.query(query_embeddings = description_embedding,n_results=2) 
        # Extract distances and ids
        distances = result['distances'][0]
        ids = result['ids'][0]
        
        # Combine distances and ids into a list of tuples for sorting
        combined = list(zip(distances, ids))
        
        # Sort the combined list by distances in decreasing order
        sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True)

        # Separate the sorted distances and ids
        sorted_distances, sorted_ids = zip(*sorted_combined)
        # Limit the results to number_of_images
        if len(sorted_ids) > number_of_images:
            sorted_ids = sorted_ids[:number_of_images]
            sorted_distances = sorted_distances[:number_of_images]

        # Prepare the sorted result
        sorted_result = {
            "ids": list(sorted_ids),
            "distances": list(sorted_distances),
        }

        return sorted_result
       
        


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