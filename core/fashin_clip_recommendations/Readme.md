<div align="center">
<h1 align="center"Fashion Recommendation System (SAAS)</h1>
<h3 align="center">Sample Project with base usage and deployment</h3>
</div>
<p align="center">
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://www.django-rest-framework.org/" target="_blank"> <img src="https://img.icons8.com/?size=100&id=xeyzFtrzVyPM&format=png&color=000000" alt="rest-framework" width="40" height="40"/> </a>
<a href="https://redis.io/" target="_blank"> <img src="https://img.icons8.com/?size=100&id=FMw01QDk8Qlu&format=png&color=000000" alt="redis" width="40" height="40"/> </a>
<a href="https://docs.celeryq.dev/en/stable//" target="_blank"> <img src="https://docs.celeryq.dev/en/stable/_static/celery_512.png" alt="celery" width="40" height="40"/> </a>
<a href="https://www.postgresql.org/" target="_blank"> <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNIa2GjsExd_GZmrCCI1G2ZJ6rGLQZoMa4WA&s" alt="Postgresql" width="40" height="40"/> </a>
<a href="https://huggingface.co/" target="_blank"> <img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" alt="huggingface" width="40" height="40"/> </a>
<a href="https://en.wikipedia.org/wiki/Recommender_system" target="_blank"> <img src="https://static.vecteezy.com/system/resources/previews/026/226/891/non_2x/recommendation-engine-icon-illustration-vector.jpg" alt="Recommender_system" width="40" height="40"/> </a>
<a href=https://en.wikipedia.org/wiki/Machine_learning" target="_blank"> <img src="https://img.freepik.com/premium-vector/ai-generate-icon-machine-learning-micropchip-symbol-ml-icon-artificial-intelligence-sign-vector_246263-31.jpg" alt="Machine learning" width="40" height="40"/> </a>
<a href="https://www.trychroma.com/" target="_blank"> <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSny5rpw45p_mya_So_dqeY-AJDQdNO-ZCu4w&s" alt="Chromadb" width="40" height="40"/> </a>



</p>

# Fashion Recommendation Backend API (SAAS)

This project provides a Backend API for a clothing recommender system, designed for online shops. It is built using Django Rest Framework and leverages Docker Compose for deployment. The system uses a SaaS model, delivering API keys to clothing online shops, allowing them to create image collections and generate recommendations based on user prompts.

## Features

- **SAAS Architecture**: Multi-tenant API key management for clothing shops.
- **Image & Text Embeddings**: CLIP model generates vectors for images/prompts.
- **Vector Database**: ChromaDB stores embeddings (collections = API keys).
- **Async Processing**: Celery workers handle embedding generation.
- **Dockerized**: Fully containerized with PostgreSQL, Redis, ChromaDB, and pgAdmin.

## Tech Stack

- **Backend**: Django REST Framework
- **AI Model**: `patrickjohncyh/fashion-clip` (CLIP for fashion)
- **Database**: PostgreSQL (relational data), ChromaDB (vector storage)
- **Queue**: Redis + Celery
- **Infrastructure**: Docker Compose

---

## Database Schema

### Entities
```plainText
├── Category
│   ├─ CategoryId (PK)
│   ├─ name
│   └─ description
│
├── Styles
│   ├─ StyleId (PK)
│   ├─ name
│   └─ description
│
├── AgeGroup
│   ├─ AgeGroupId (PK)
│   ├─ name
│   └─ description
│
├── ImageCollection (Core)
│   ├─ ImageID (PK)
│   ├─ APIKey (FK → List_API_Key)
│   ├─ Photo (uploaded to /Photo_collection/{api_key}/)
│   ├─ Processor_embedded (boolean)
│   ├─ ForeignKeys: Category, Styles, AgeGroup
│
└── Prompt_API
    ├─ PromptID (PK)
    ├─ APIKey (FK → List_API_Key)
    ├─ prompt (text)
    └─ number_recommended_images

 

 ```


---
## Workflow
### Shop Registration
   Shops obtain an API key 

### Image Collection Upload
  Upload all images  they want to recommend to users .
  
  ```POST /api/images/
      Body: { "photo": File, "api_key": "shop_123", name : "name of photo" }
  ```


### Embedding Generation
for every image we must create embedding vector and store in chromadb. the collection name in chromadb is equal to API Key of online shops 

Resizes image → generates CLIP embedding → stores in ChromaDB.

### Recommendation Query
When users in online shops want to yser recommender systems , they enter prompt and the number of images they want to recommend.
```GET /api/recommend/
Body: { "prompt": "summer dress", "api_key": "shop_123", "num_results": 5 }

```


## Infrastructure Diagram
```graph TD
  A[Django Backend] -->|Stores Metadata| B[(PostgreSQL)]
  A -->|Async Tasks| C[Redis]
  C -->|queue_two| D[Celery Worker]
  D -->|CLIP Model| E[(ChromaDB)]
  A -->|Query Embeddings| E
  E -->|API Key = Collection| A
  ```

## Getting Started
### Prerequisites
```
Docker
Python 3.9+
```
### Setup

#### Clone the repository
```bash
git clone https://github.com/yourusername/FitMatchFinder.git
```

#### Create .env file:
```bash
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
```
#### Run
```bash
docker-compose up --build
```
### Access services:

- Django API: http://localhost:8000
- pgAdmin: http://localhost:5050
- ChromaDB: http://chromadb:8001




###  API Endpoints
```
| Endpoint                           | Method              | Description                                      |
|---------------------------|--------|------------------------------------------------- ----------------------|
| `/images/<str:api_key>/`           | GET                  | List all images for the specified API key       |
| `/images/<str:api_key>/`           | POST                 | Upload image + trigger embedding task           |
| `/images/<str:api_key>/<int:pk>/`  | PUT , Delete, GET    |  Retrieve details of a specific image|          |
| `/api/prompts/`                    | POST                 | Submit a prompt to obtain image recommendations |

```
### Task Processing (Celery)
Queues: queue_two (dedicated worker)

#### Tasks:

- CreateEmbedding: Image → CLIP → ChromaDB

- DeleteEmbedding: Remove embeddings on image delete (when online shops remove or finish these clothes from the online shops so these clothes do not recommend to customers in online shops )

- Fashion_clip_recommender: Handle recommendation queries (for giving recommend to customers )

Monitor tasks via Flower or Django admin.


### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

