Clothing Online Shop Recommender System - Backend API

This project provides a Backend API for a clothing online shop recommender system. It is built using Django Rest Framework and leverages Docker Compose for deployment. The system uses the FashionCLIP model to generate embeddings for images and text, which are stored and queried using ChromaDB. The system is designed as a SaaS platform, delivering API keys to clothing online shops, allowing them to create image collections and get recommendations based on user prompts.

Features
Image Collection Management: Online shops can create and manage image collections using the ImageCollection model.

Embedding Generation: Images are processed using the FashionCLIP model to generate embeddings, which are stored in ChromaDB.

Text-to-Image Recommendations: Users can enter a text prompt (e.g., "red dress with floral patterns"), and the system will return relevant images from the collection.

Celery Workers: All image processing and embedding tasks are handled asynchronously using Celery workers.

Dockerized Deployment: The entire system is containerized using Docker Compose for easy deployment and scalability.

Database Diagram
Below is the database diagram for the models used in this application:

plaintext
Copy
+-------------------+       +-------------------+       +-------------------+
|    Category       |       |      Styles       |       |     AgeGroup      |
+-------------------+       +-------------------+       +-------------------+
| CategoryId (PK)   |       | StyleId (PK)      |       | AgeGroupId (PK)   |
| name              |       | name              |       | name              |
| description       |       | description       |       | description       |
+-------------------+       +-------------------+       +-------------------+
        |                         |                         |
        |                         |                         |
        |                         |                         |
        |                         |                         |
        |                         |                         |
+-------------------+       +-------------------+       +-------------------+
|  ImageCollection  |       |   List_API_Key    |       |   Prompt_API      |
+-------------------+       +-------------------+       +-------------------+
| ImageID (PK)      |       | APIKey (PK)       |       | PromptID (PK)     |
| APIKey (FK)       |<------| key               |       | APIKey (FK)       |
| Photo             |       +-------------------+       | prompt            |
| name              |                                  | num_recommended   |
| description       |                                  +-------------------+
| Category (FK)     |
| Styles (FK)       |
| AgeGroup (FK)     |
| Processor_embedded|
+-------------------+
Setup Instructions
Prerequisites
Docker and Docker Compose installed on your machine.

Python 3.8 or higher.

Steps to Run the Application
Clone the Repository:

bash
Copy
git clone <repository-url>
cd <repository-folder>
Set Up Environment Variables:
Create a .env file in the root directory and add the following variables:

plaintext
Copy
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
PGADMIN_DEFAULT_EMAIL=your_email
PGADMIN_DEFAULT_PASSWORD=your_password
Build and Run the Docker Containers:

bash
Copy
docker-compose up --build
Access the Services:

Django Backend: http://localhost:8000

PostgreSQL Database: localhost:5432

PgAdmin: http://localhost:5050

Redis: localhost:6379

ChromaDB: localhost:8001

SMTP4Dev: http://localhost:5000

Run Celery Workers:
The Celery workers are already configured to run with the Docker Compose setup. You can monitor the workers using the logs.

API Endpoints
Image Collection Management
Create Image Collection:

Endpoint: POST /api/image-collection/

Description: Create a new image collection.

Request Body:

json
Copy
{
  "APIKey": "your_api_key",
  "Photo": "image_file",
  "name": "Image Name",
  "description": "Image Description",
  "Category": 1,
  "Styles": 1,
  "AgeGroup": 1
}
Get Image Collection:

Endpoint: GET /api/image-collection/<image_id>/

Description: Retrieve details of a specific image collection.

Text-to-Image Recommendations
Get Recommendations:

Endpoint: POST /api/recommendations/

Description: Get image recommendations based on a text prompt.

Request Body:

json
Copy
{
  "api_key": "your_api_key",
  "prompt": "A red dress with floral patterns",
  "number_of_images": 5
}
Celery Tasks
The following Celery tasks are available for asynchronous processing:

CreateEmbedding: Generates embeddings for images and stores them in ChromaDB.

DeleteEmbedding: Deletes embeddings from ChromaDB.

RetrieveImageIds: Retrieves all image IDs from a specific collection in ChromaDB.

FashionClipRecommender: Provides image recommendations based on a text prompt.

Technologies Used
Django: Backend framework for building the API.

Django Rest Framework: For building RESTful APIs.

PostgreSQL: Database for storing application data.

Redis: Message broker for Celery tasks.

ChromaDB: Vector database for storing image embeddings.

Docker: Containerization for easy deployment.

Celery: Asynchronous task queue for processing image embeddings.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.