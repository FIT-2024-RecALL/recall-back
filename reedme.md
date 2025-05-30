## Overview

## Purpose and Scope

This document provides a high-level introduction to the RecALL backend system, a FastAPI-based flashcard and spaced repetition learning platform. It covers the system's purpose, key features, architectural approach, and core components. For detailed information about specific subsystems, see [Deployment and Infrastructure](https://deepwiki.com/FIT-2024-RecALL/recall-back/2-deployment-and-infrastructure), [Application Architecture](https://deepwiki.com/FIT-2024-RecALL/recall-back/3-application-architecture), [Core Domain Models](https://deepwiki.com/FIT-2024-RecALL/recall-back/4-core-domain-models), and [API Reference](https://deepwiki.com/FIT-2024-RecALL/recall-back/5-api-reference).

## System Description

RecALL is a web-based learning platform backend that implements flashcard-style studying with spaced repetition algorithms and AI-powered feedback. The system enables users to create flashcards, organize them into collections, attach files, and track learning progress through scientifically-backed spaced repetition techniques.

The platform supports both private learning and public content sharing, allowing users to create personal study materials or contribute to a shared knowledge base. AI integration via Ollama provides intelligent feedback and scoring during study sessions.

## Key Features

| Feature Category | Capabilities |
| --- | --- |
| **User Management** | Registration, authentication, profile management |
| **Content Creation** | Flashcard creation with front/back sides, rich text support |
| **Organization** | Collections to group related cards, public/private visibility |
| **File Attachments** | Upload and attach images/documents to cards via MinIO storage |
| **Learning System** | Spaced repetition algorithm, progress tracking, training records |
| **AI Integration** | Automated feedback and scoring via Ollama LLM service |
| **Content Sharing** | Public collections and cards for community learning |
| **Multi-tenancy** | User-owned content with proper access controls |

Sources: [README.md3-10](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/README.md#L3-L10) [config/ollama.env](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/config/ollama.env) [compose.yaml79-135](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/compose.yaml#L79-L135)

## Architecture Overview

The system follows a microservices architecture deployed via Docker Compose, with clear separation between presentation, business logic, and data layers. The application implements repository and service layer patterns for clean code organization.

### High-Level System Architecture

```
StorageData ServicesApplication LayerInfrastructure LayerExternalUsers via Web Frontendnginx:1.27.3-alpineReverse Proxy & SSLcertbot/certbotSSL Certificate ManagementFrontend ContainerPort 8080FastAPI Backendapp.main:appPort 8000, 2 workerspostgres:17.0-alpinerecall_db databaseminio/minioObject StoragePorts 9000/9001ollama/ollamaLLM ServicePort 11434recall-pgdata-volumerecall-minio-volumerecall-ollama-volume
```

Sources: [compose.yaml1-153](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/compose.yaml#L1-L153) [app/main.py22-33](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/main.py#L22-L33) [config/nginx.conf33-39](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/config/nginx.conf#L33-L39)

### Application Request Flow

```
Data LayerBusiness LayerAPI LayerUserAPI/users endpointsCardAPI/cards endpointsCollectionAPI/collections endpointsStorageAPI/storage endpointsTrainAPI/train_records endpointsUserServiceAuthentication & ProfileCardServiceCard CRUD & ManagementCollectionServiceCollection ManagementStorageServiceFile Upload/DownloadTrainRecordServiceProgress TrackingRepository PatternBaseSQLAlchemyRepositoryUnit of WorkTransaction ManagementSQLAlchemy ModelsUser, Card, Collection, File
```

Sources: [app/main.py32-33](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/main.py#L32-L33) [app/api](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/api) [README.md5-9](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/README.md#L5-L9)

## Technology Stack

The system is built on modern Python web technologies with a focus on type safety, performance, and maintainability:

| Component | Technology | Purpose |
| --- | --- | --- |
| **Web Framework** | FastAPI | High-performance async API framework with automatic OpenAPI docs |
| **Database ORM** | SQLAlchemy | Python SQL toolkit and ORM for database interactions |
| **Data Validation** | Pydantic | Data validation and settings management used by FastAPI |
| **Database** | PostgreSQL 17.0 | Primary relational database for application data |
| **Object Storage** | MinIO | S3-compatible storage for file attachments |
| **AI/ML** | Ollama | Local LLM server for AI feedback (llama3.1, mistral) |
| **Web Server** | Nginx | Reverse proxy with SSL termination |
| **Containerization** | Docker + Docker Compose | Multi-service deployment orchestration |
| **Package Management** | Poetry | Python dependency management and packaging |

Sources: [README.md5-9](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/README.md#L5-L9) [Dockerfile2-44](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/Dockerfile#L2-L44) [config/ollama.env](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/config/ollama.env)

## System Components

### Core Services

The application runs as multiple Docker containers with specific responsibilities:

| Service | Container | Purpose | Health Check |
| --- | --- | --- | --- |
| **nginx** | `recall-nginx` | SSL termination, reverse proxy, static file serving | N/A |
| **backend** | `recall-backend` | FastAPI application, business logic, API endpoints | N/A |
| **frontend** | `recall-frontend` | Web UI application | `curl -f http://127.0.0.1:8080/` |
| **postgres** | `recall-postgres` | Primary database for user data, cards, collections | `pg_isready -U backend -d recall_db` |
| **minio** | `recall-minio` | Object storage for file attachments | `curl -f http://localhost:9000/minio/health/live` |
| **ollama** | `recall-ollama` | LLM service for AI feedback | N/A |

### Application Lifecycle

The FastAPI application implements comprehensive lifecycle management in [\`app/main.py11-19](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/%60app/main.py#L11-L19):

1.  **Startup**: Creates database tables, verifies MinIO bucket availability, loads AI model
2.  **Runtime**: Serves API requests with CORS middleware for cross-origin requests
3.  **Shutdown**: Unloads AI model, closes database connections

```
Application Startupcreate_db_tables()is_bucket_available()load_model()Serve RequestsApplication Shutdownunload_model()close_db_connections()
```

Sources: [app/main.py11-19](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/main.py#L11-L19) [compose.yaml44-61](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/compose.yaml#L44-L61)

## Deployment Model

The system is designed for production deployment with the following characteristics:

-   **Multi-container Architecture**: Each service runs in its own container with resource limits
-   **SSL/TLS Security**: Automatic certificate management via Let's Encrypt and Certbot
-   **High Availability**: Health checks and restart policies for service reliability
-   **Scalability**: Backend configured with 2 Uvicorn workers and 8GB memory limit
-   **Data Persistence**: Named volumes for database, object storage, and AI model data
-   **Network Isolation**: Internal Docker network for service communication

The system serves production traffic at `letsrecall.ru` with CORS configured for the domain and local development endpoints.

Sources: [compose.yaml1-153](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/compose.yaml#L1-L153) [config/nginx.conf1-43](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/config/nginx.conf#L1-L43) [app/main.py23-29](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/app/main.py#L23-L29)