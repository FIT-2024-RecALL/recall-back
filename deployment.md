# Deployment and Infrastructure

This document covers the deployment architecture, Docker-based infrastructure, and production setup for the RecAll flashcard learning platform. It details the multi-service containerized deployment using Docker Compose, including reverse proxy configuration, SSL termination, persistent storage setup, and service orchestration.

For information about application architecture and code organization, see [Application Architecture](https://deepwiki.com/FIT-2024-RecALL/recall-back/3-application-architecture). For specific service configuration details, see [Configuration and Environment Setup](https://deepwiki.com/FIT-2024-RecALL/recall-back/6-configuration-and-environment-setup).

## Deployment Architecture Overview

The RecAll platform deploys as a multi-container application orchestrated by Docker Compose. The infrastructure consists of seven main services with nginx serving as the reverse proxy and SSL termination point.

```
Persistent StorageDocker Network: devExternalInternet Trafficletsrecall.ruLet's EncryptSSL Certificate Authoritynginx:1.27.3-alpineContainer: recall-nginxPorts: 80, 443certbot/certbot:latestContainer: certbotFrontend ServiceContainer: recall-frontendPort: 8080FastAPI BackendContainer: recall-backendPort: 8000postgres:17.0-alpineContainer: recall-postgresPort: 5432minio/minio:latestContainer: recall-minioPorts: 9000, 9001ollama/ollamaContainer: recall-ollamaPort: 11434minio/mc:latestContainer: recall-minio-setupCustom Setup ContainerContainer: recall-ollama-setupSSL Certificates$CERTBOT_PATHPostgreSQL Data$POSTGRES_VOLUME_PATHObject Storage$MINIO_VOLUME_PATHLLM Models$OLLAMA_VOLUME_PATH
```

## Docker Compose Service Architecture

The deployment uses a named Docker Compose project called `recall` with all services connected via the `dev` network. Services are configured with health checks, restart policies, and dependency management.

### Core Application Services

| Service | Container Name | Image/Build | Ports | Dependencies |
| --- | --- | --- | --- | --- |
| `nginx` | `recall-nginx` | `nginx:1.27.3-alpine` | 80, 443 | frontend, backend |
| `frontend` | `recall-frontend` | Built from `$RECALL_FRONTEND_PATH` | 8080 | \- |
| `backend` | `recall-backend` | Built from `.` (Dockerfile) | 8000 | postgres, minio |

### Data and Infrastructure Services

| Service | Container Name | Image | Ports | Purpose |
| --- | --- | --- | --- | --- |
| `postgres` | `recall-postgres` | `postgres:17.0-alpine` | 5432 | Primary database |
| `minio` | `recall-minio` | `minio/minio:latest` | 9000, 9001 | Object storage |
| `ollama` | `recall-ollama` | `ollama/ollama` | 11434 | LLM inference |

### Setup and Utility Services

| Service | Container Name | Image/Build | Purpose |
| --- | --- | --- | --- |
| `certbot` | \- | `certbot/certbot:latest` | SSL certificate management |
| `minio-setup` | `recall-minio-setup` | `minio/mc:latest` | MinIO bucket initialization |
| `ollama-setup` | `recall-ollama-setup` | Custom build | Model deployment |

## Container Build and Resource Configuration

### Backend Container Build Process

The backend service uses a multi-stage Docker build optimized for production deployment:

```
Runtime StageBuilder Stagepython:3.12.10Poetry 1.8.1Dependency ManagementVirtual Environment/code/.venvpython:3.12.10uvicorn--workers 2--limit-max-requests 1000Application Code./config ./app
```

The backend container is configured with:

-   **Memory Limit**: 8GB maximum (`deploy.resources.limits.memory`)
-   **Workers**: 2 Uvicorn worker processes
-   **Request Limit**: 1000 requests per worker before restart
-   **Port**: Exposes port 8000 internally

### Nginx Reverse Proxy Configuration

The nginx service handles SSL termination and request routing:

```
SSL ConfigurationNginx ConfigurationHTTP :80letsrecall.ruUnsupported markdown: linkHTTPS :443letsrecall.ruACME Challenge/.well-known/acme-challenge/Frontend Proxy/ → frontend:8080API Proxy/api/ → backend:8000SSL Certificate/etc/nginx/ssl/live/letsrecall.ru/fullchain.pemSSL Private Key/etc/nginx/ssl/live/letsrecall.ru/privkey.pem
```

Key nginx features:

-   **HTTP to HTTPS Redirect**: All HTTP traffic redirected to HTTPS
-   **Client Body Size**: Maximum 10MB uploads (`client_max_body_size`)
-   **API Routing**: `/api/` requests routed to backend service
-   **Frontend Routing**: All other requests routed to frontend service

## Persistent Volume Configuration

The deployment uses bind-mounted volumes for persistent data storage, configured via environment variables:

```
Container MountsHost Filesystem$CERTBOT_PATHSSL Certificates$POSTGRES_VOLUME_PATHDatabase Files$MINIO_VOLUME_PATHObject Storage$OLLAMA_VOLUME_PATHLLM Models/etc/nginx/ssl//var/www/certbot//var/lib/postgresql/data/mnt/minio-volume/root/.ollama
```

Volume configuration uses `driver_opts` with bind mounting:

-   **Type**: `none` (bind mount)
-   **Options**: `bind`
-   **Device**: Environment variable path

## Health Checks and Service Dependencies

The deployment implements comprehensive health monitoring and startup orchestration:

### Health Check Configuration

| Service | Health Check Command | Interval | Timeout | Retries |
| --- | --- | --- | --- | --- |
| `frontend` | `curl -f http://127.0.0.1:8080/` | 30s | 10s | 3 |
| `postgres` | `pg_isready -U backend -d recall_db` | 3s | 3s | 5 |
| `minio` | `curl -f http://localhost:9000/minio/health/live` | 30s | 10s | 3 |

### Service Dependency Chain

```
postgrescondition: service_healthyminiocondition: service_healthybackenddepends_on: postgres, miniofrontendindependent startupnginxdepends_on: frontend, backendminio-setupdepends_on: minio healthyollama-setupdepends_on: ollama
```

## Environment Configuration Requirements

The deployment requires multiple configuration files in the `config/` directory:

### Required Configuration Files

| File | Purpose | Key Variables |
| --- | --- | --- |
| `auth.env` | Authentication configuration | `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_KEY` |
| `postgres.env` | Database connection | `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` |
| `minio-backend.env` | Object storage client | `MINIO_HOSTNAME`, `MINIO_BUCKET_NAME`, `MINIO_LOGIN` |
| `minio-server.env` | Object storage server | `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD` |
| `ollama.env` | LLM service configuration | `OLLAMA_HOSTNAME`, `OLLAMA_MODEL` |

### Deployment Environment Variables

The Docker Compose deployment requires these environment variables:

| Variable | Purpose | Example |
| --- | --- | --- |
| `CERTBOT_PATH` | SSL certificate storage | `/opt/certbot` |
| `RECALL_FRONTEND_PATH` | Frontend source code | `/opt/recall-front` |
| `MINIO_VOLUME_PATH` | Object storage data | `/opt/minio-data` |
| `POSTGRES_VOLUME_PATH` | Database storage | `/opt/postgres-data` |
| `OLLAMA_VOLUME_PATH` | LLM model storage | `/opt/ollama-data` |
