# Configration and Environment Setup 

This document covers the environment configuration, dependency management, and setup procedures for the recall-back application. It details the required configuration files, environment variables, and setup processes for both local development and Docker deployment scenarios.

For information about the application architecture and service layer setup, see [Application Architecture](https://deepwiki.com/FIT-2024-RecALL/recall-back/3-application-architecture). For deployment infrastructure details, see [Docker Compose Services](https://deepwiki.com/FIT-2024-RecALL/recall-back/2.1-docker-compose-services).

## Environment Configuration Files

The application requires several environment configuration files located in the `config/` directory. These files configure authentication, database connections, object storage, and AI services.

### Core Configuration Files

#### Authentication Configuration

The `auth.env` file configures JWT authentication and session management:

```
SECRET_KEY=<secret_key_for_encrypting>
ALGORITHM=<encrypting_algorithm: e.g. HS256>
ACCESS_TOKEN_KEY=<title_of_cookie_token_attribute>
EXPIRE_HOURS=12
HTTPONLY=true
SECURE=true
SAMESITE=strict # or lax or none
```

#### Database Configuration

The `postgres.env` file configures PostgreSQL database connections:

```
POSTGRES_USER=<backend_postgres_user_login>
POSTGRES_PASSWORD=<backend_postgres_user_passwrod>
POSTGRES_HOST=<postgres_addr>
POSTGRES_HOST_PORT=<postgres_port>
POSTGRES_DB=<postgres_db_name>
```

#### Object Storage Configuration

The `minio-backend.env` file configures MinIO S3-compatible storage for the backend:

```
MINIO_HOSTNAME=<minio_addr> # IP address - without protocol
MINIO_PORT=<minio_port>
MINIO_BUCKET_NAME=<bucket_name>
MINIO_LOGIN=<backend_minio_user_login>
MINIO_PASSWORD=<backend_minio_user_password>
MINIO_MAX_FILE_MB_SIZE=<mb_integer_number>
```

#### AI Service Configuration

The `ollama.env` file configures the Ollama LLM service:

```
OLLAMA_FROM_MODEL=<basic_model> # now allowed llama3.1 and mistral
OLLAMA_HOSTNAME=<ollama_addr> # IP address - without protocol
OLLAMA_PORT=<port>
OLLAMA_MODEL=<name_for_modified_model>
```

### Deployment-Specific Configuration

For Docker deployment, additional configuration files are required:

#### MinIO Server Configuration

The `minio-server.env` file configures MinIO server settings:

```
MINIO_ROOT_USER="<root_user_login>"
MINIO_ROOT_PASSWORD="<root_user_passwrod>"
MINIO_VOLUMES="/mnt/minio-volume"
MINIO_OPTS="--console-address :9001"
```

#### Environment Variables for Docker Compose

The following environment variables must be set for Docker deployment:

| Variable | Purpose | Example |
| --- | --- | --- |
| `CERTBOT_PATH` | SSL certificates directory | `/etc/letsencrypt` |
| `RECALL_FRONTEND_PATH` | Frontend source code path | `/path/to/recall-front` |
| `MINIO_VOLUME_PATH` | MinIO storage directory | `/data/minio` |
| `POSTGRES_VOLUME_PATH` | PostgreSQL data directory | `/data/postgres` |
| `OLLAMA_VOLUME_PATH` | Ollama models directory | `/data/ollama` |

**Configuration File Structure**

```
Application ServicesDeployment ConfigurationRequired Configuration Filesauth.envJWT & Session Configpostgres.envDatabase Connectionminio-backend.envStorage Accessollama.envAI Service Configminio-server.envStorage ServerEnvironment VariablesVolume Paths & SSLFastAPI BackendMinIO StoragePostgreSQL DatabaseOllama LLM
```

Sources: [README.md18-57](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/README.md#L18-L57) [compose.yaml67-153](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/compose.yaml#L67-L153)

## Python Dependencies and Poetry Setup

The application uses Poetry for Python dependency management and virtual environment handling.

### Core Dependencies

The project requires Python 3.11+ and uses these primary dependencies:

| Package | Version | Purpose |
| --- | --- | --- |
| `fastapi[standard]` | ^0.115.3 | Web framework with standard features |
| `sqlalchemy` | ^2.0.36 | Database ORM |
| `asyncpg` | ^0.30.0 | Async PostgreSQL driver |
| `pydantic-settings` | ^2.6.1 | Configuration management |
| `python-jose` | ^3.3.0 | JWT token handling |
| `bcrypt` | ^4.2.0 | Password hashing |
| `ollama` | ^0.4.7 | AI/LLM integration |
| `miniopy-async` | ^1.22.1 | Async MinIO client |

### Poetry Installation and Setup

Poetry must be installed before setting up the development environment:

```
# Install Poetry (see official documentation)
curl -sSL https://install.python-poetry.org | python3 -

# Verify installation
poetry --version
```

### Development Environment Setup

1.  **Create and activate virtual environment:**

```
cd <path_to_the_project>
poetry shell
```

2.  **Install dependencies:**

```
poetry install
```

3.  **Verify installation:**

```
poetry show  # List installed packages
```

**Dependency Management Flow**

```
Development Commandspyproject.tomlDependency Specspoetry.lockLocked VersionsVirtual EnvironmentIsolated Pythonpoetry installpoetry shellpoetry add poetry update
```

Sources: [pyproject.toml1-29](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/pyproject.toml#L1-L29) [README.md11-16](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/README.md#L11-L16) [poetry.lock1-50](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/poetry.lock#L1-L50)

## Local Development Setup

Local development setup enables running the FastAPI application directly without Docker for faster development cycles.

### Prerequisites

1.  **Poetry installed** (see previous section)
2.  **PostgreSQL running locally** or accessible remotely
3.  **MinIO server running** (optional for file operations)
4.  **Ollama service running** (optional for AI features)

### Environment Configuration

1.  **Create configuration directory:**

```
mkdir config
```

2.  **Create required environment files** as described in the Environment Configuration Files section
    
3.  **Ensure external services are accessible** with the hostnames and ports specified in the configuration files
    

### Running the Application

The application can be started using several methods:

**Development mode with hot reload:**

```
fastapi dev app/main.py
```

**Production-style execution:**

```
# Method 1: Module execution
python -m app.main

# Method 2: Direct uvicorn
uvicorn app.main:app --<your_flags>
```

### Development Workflow

**Local Development Setup Flow**

```
External ServicesNoYesNoYesStart DevelopmentPoetry Installed?Install PoetryCreate config/ directoryAdd .env filesauth.env, postgres.env, etc.poetry shellpoetry installExternal ServicesRunning?Start PostgreSQL,MinIO, Ollamafastapi dev app/main.pyDevelopment ReadyHot Reload EnabledPostgreSQL:5432MinIO:9000Ollama:11434
```

Sources: [README.md58-76](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/README.md#L58-L76) [pyproject.toml9-24](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/pyproject.toml#L9-L24)

## Docker Deployment Configuration

Docker deployment uses `compose.yaml` to orchestrate multiple services including the web server, application, database, storage, and AI services.

### Service Architecture

The Docker Compose configuration defines these services:

| Service | Container | Purpose | Dependencies |
| --- | --- | --- | --- |
| `nginx` | `recall-nginx` | Reverse proxy & SSL | `frontend`, `backend` |
| `backend` | `recall-backend` | FastAPI application | `postgres`, `minio` |
| `frontend` | `recall-frontend` | Frontend application | None |
| `postgres` | `recall-postgres` | PostgreSQL database | None |
| `minio` | `recall-minio` | Object storage server | None |
| `ollama` | `recall-ollama` | LLM service | None |

### Network and Volume Configuration

**Network Setup:**

-   All services use the `dev` network for internal communication
-   External access through nginx on ports 80/443

**Volume Mounting:**

```
volumes:
  recall-minio-volume:
    driver_opts:
      type: none
      o: bind
      device: $MINIO_VOLUME_PATH
  recall-pgdata-volume:
    driver_opts:
      type: none
      o: bind
      device: $POSTGRES_VOLUME_PATH
  recall-ollama-volume:
    driver_opts:
      type: none
      o: bind
      device: $OLLAMA_VOLUME_PATH
```

### Deployment Process

1.  **Prepare environment variables:**

```
export CERTBOT_PATH=/path/to/certificates
export RECALL_FRONTEND_PATH=/path/to/frontend
export MINIO_VOLUME_PATH=/path/to/minio/storage
export POSTGRES_VOLUME_PATH=/path/to/postgres/data
export OLLAMA_VOLUME_PATH=/path/to/ollama/models
```

2.  **Create configuration files** in `config/` directory
    
3.  **Build and start services:**
    

```
docker compose up --build
```

4.  **SSL certificate setup (if needed):**

```
# Initial certificate creation
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d <domain.addr>

# Certificate renewal
docker compose run --rm certbot renew
```

**Docker Service Dependencies**

```
Persistent StorageData ServicesApplication LayerFrontend LayerExternal TrafficInternet:80, :443nginxrecall-nginxReverse ProxycertbotSSL Managementfrontendrecall-frontend:8080backendrecall-backend:8000FastAPI Apppostgresrecall-postgres:5432miniorecall-minio:9000/:9001ollamarecall-ollama:11434minio-setuprecall-minio-setupInitializationollama-setuprecall-ollama-setupModel Setuprecall-minio-volume$MINIO_VOLUME_PATHrecall-pgdata-volume$POSTGRES_VOLUME_PATHrecall-ollama-volume$OLLAMA_VOLUME_PATHSSL Certificates$CERTBOT_PATH
```

Sources: [compose.yaml1-153](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/compose.yaml#L1-L153) [README.md78-105](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/README.md#L78-L105)

## Service-Specific Configuration

Each service in the deployment stack requires specific configuration for optimal operation.

### Backend Service Configuration

The backend service uses these key configuration aspects:

**Resource Limits:**

```
deploy:
  resources:
    limits:
      memory: 8G
```

**Health Dependencies:**

-   Waits for PostgreSQL health check: `pg_isready -U backend -d recall_db`
-   Waits for MinIO health check: `curl -f http://localhost:9000/minio/health/live`

### PostgreSQL Configuration

**Health Check:**

```
healthcheck:
  test: "pg_isready -U backend -d recall_db"
  interval: 3s
  timeout: 3s
  start_period: 5s
  retries: 5
```

**Environment:** Configured via `postgres.env` file

### MinIO Configuration

**Server Setup:**

-   Console address: `:9001`
-   API address: `:9000`
-   Configuration loaded from `minio-server.env`

**Backend Access:**

-   Configured via `minio-backend.env`
-   Setup script: `minio-setup.sh`

### Ollama Configuration

**Model Management:**

-   Custom model setup via `ollama-setup` container
-   Base models: `llama3.1`, `mistral`
-   Custom model naming via `OLLAMA_MODEL` environment variable

**Service Initialization Flow**

```
Configuration FilesNoYesNoYesdocker compose upStart Core Servicespostgres, minio, ollamaHealth Checks Pass?Wait & RetryStart Setup Servicesminio-setup, ollama-setupminio-setupCreate buckets & usersollama-setupDownload & configure modelsSetup Complete?restart: on-failureStart Application Servicesbackend, frontendStart nginxReverse ProxyDeployment Readypostgres.envminio-server.envminio-backend.envollama.env
```

Sources: [compose.yaml44-135](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/compose.yaml#L44-L135) [README.md94-105](https://github.com/FIT-2024-RecALL/recall-back/blob/fd0685d4/README.md#L94-L105)