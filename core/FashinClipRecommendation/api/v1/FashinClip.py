import torch
import chromadb
from PIL import Image
import numpy as np
from transformers import AutoProcessor, AutoModelForZeroShotImageClassification


class FashionImageRecommender:
    def __init__(self, chroma_client):
        self.model = AutoModelForZeroShotImageClassification.from_pretrained("patrickjohncyh/fashion-clip")
        self.chroma_client = chroma_client
        self.image_embeddings = []
        self.image_ids = []

    def load_images(self, image_paths):
        """Loads images and creates embeddings."""
        for idx, image_path in enumerate(image_paths):
            image = Image.open(image_path).convert("RGB")
            embedding = self.create_embedding(image)
            self.image_embeddings.append(embedding)
            self.image_ids.append(idx)  # or any unique identifier for each image

        # Store embeddings in Chroma
        self.chroma_client.add(self.image_ids, self.image_embeddings)

    def create_embedding(self, image):
        """Generates an embedding for a given image."""
        # Preprocess the image as required by the model
        image = self.preprocess_image(image)
        with torch.no_grad():
            embedding = self.model(image)
        return embedding.numpy()

    def preprocess_image(self, image):
        """Preprocess the image for the model."""
        # Add your preprocessing steps here (resize, normalize, etc.)
        image = image.resize((224, 224))  # Example resize
        image_tensor = torch.tensor(np.array(image)).float() / 255.0
        image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0)  # Change to CxHxW
        return image_tensor

    def recommend_images(self, description):
        """Recommends images based on the user's description."""
        description_embedding = self.create_description_embedding(description)
        similarities = self.chroma_client.query(description_embedding)
        
        # Sort and get the top recommendations
        recommended_images = sorted(similarities, key=lambda x: x['similarity'], reverse=True)
        return recommended_images[:5]  # Return top 5 recommendations

    def create_description_embedding(self, description):
        """Generates an embedding for a given description."""
        # You need a method to generate embeddings for text descriptions
        # This could be a separate model or the same one if it supports text
        with torch.no_grad():
            embedding = self.model.encode_text(description)  # Example method
        return embedding.numpy()

# Example usage
if __name__ == "__main__":
    # Load your Fashion Clip model
    model = ...  # Load your model here
    chroma_client = chromadb.Client()

    recommender = FashionImageRecommender(model, chroma_client)

    # Load your images
    image_paths = ['path/to/image1.jpg', 'path/to/image2.jpg']
    recommender.load_images(image_paths)

    # Get recommendations based on user description
    user_description = "A red dress with floral patterns"
    recommendations = recommender.recommend_images(user_description)
    print(recommendations)
