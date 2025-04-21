# FitMatchFinder - AI SaaS Platform for Online Shops

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)

FitMatchFinder is an AI-powered SaaS platform designed specifically for online shops, featuring embedded machine learning models for enhanced e-commerce experiences. The platform includes multiple integrated applications that work together to provide authentication, clothing recommendations, and document analysis capabilities.

## Key Features

- **Custom Authentication System**: Secure and flexible user and API Key management
- **FashinClip Recommendation**: AI-powered clothing recommendation engine
- **Customized RAG Pipeline**: Fast document analysis for product catalogs (40% faster than traditional RAG)
- **Containerized Deployment**: Easy setup with Docker Compose
- **Comprehensive Documentation**: Built with Sphinx

## Applications

### 1. Custom Authentication System
A flexible authentication system that can be customized for different e-commerce needs.

🔗 [View Details](https://github.com/Ahmadzadeh920/FitMatchFinder/tree/main/core/accounts)

### 2. FashinClip Recommendation
Backend API for a sophisticated clothing recommender system using machine learning.

🔗 [View Details](https://github.com/Ahmadzadeh920/FitMatchFinder/tree/main/core/FashinClipRecommendation)

### 3. Customized RAG Pipeline
Backend API chat system for analyzing online shop catalog documents (PDFs) with enhanced performance using OpenAI and Colivara implementations.

🔗 [View Details](https://github.com/Ahmadzadeh920/FitMatchFinder/tree/main/core/customized_RAG)

## System Architecture

The platform is built using:
- Django (DRF) backend
- PostgreSQL database
- Redis for caching and task queue
- ChromaDB and Colivara for vector storage 
- OpenAI and HuggingFace for ML models 
- Celery for asynchronous task processing
- Docker for containerization

## Prerequisites

- Docker (v20.10+)
- Docker Compose (v2.0+)
- Python 3.11

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Ahmadzadeh920/FitMatchFinder.git
cd FitMatchFinder
```

### 2- Set up environment variables
Create a .env file in the root directory with the following variables:
```bash
SECRET_KEY = ''
DEBUG = "True"
SERVERNAMES = 'localhost 127.0.0.1'
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = 'db'
DB_PORT ='5432'
Domain= 'http://127.0.0.1:8000, localhost:8000, http://localhost:8000'
# pgadmin
PGADMIN_DEFAULT_EMAIL= ''
PGADMIN_DEFAULT_PASSWORD = ''

# 
PASSWORD_ACTIVE_BASE_URL=http://127.0.0.1:8000/accounts/api/v1/activate/jwt/
PASSWORD_Reset_BASE_URL=http://127.0.0.1:8000/accounts/api/v1/reset/pass/

CHROMA_DB_URL = http://chromadb:8001


API_KEY_COLIVARA = ''
API_KEY_OpenAI = ""

```

### 3- Build and start the services
```bach
docker-compose up --build
```
#### The system will be available at:

    Backend: http://localhost:8000

    Documentation: http://localhost:8002

    PGAdmin: http://localhost:5050

    ChromaDB: http://localhost:8001

    SMTP4Dev: http://localhost:5000


## Docker Services Overview
The system consists of the following services defined in docker-compose.yaml:

    Redis: For caching and task queue

    PostgreSQL: Primary database

    ChromaDB: Vector embedding database


    Backend: Django application server

    Celery Workers: Two separate workers for task processing

    SMTP4Dev: Development email server

    PGAdmin: Database administration interface

    Docs: Sphinx documentation server


 