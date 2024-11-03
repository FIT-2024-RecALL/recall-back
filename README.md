# RecAll

## Technology Stack and Features

- [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
- [SQLAlchemy](https://https://www.sqlalchemy.org/) for the Python SQL database interactions (ORM).
- [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
- [PostgreSQL](https://www.postgresql.org) as the SQL database.
- [MinIO](https://min.io/docs/minio/linux/operations/installation.html) as S3-compatible object storage with [wrapper for Python](https://min.io/docs/minio/linux/developers/python/API.html)

## Requirements
- [Docker Engine + Docker Compose](https://docs.docker.com/engine/install/)

## How to deploy
1. Go to deploy folder (*Now there're only Minio image in compose.yaml*)
2. Add config files into `minio_config/`:
  - `.env`:
```conf
MINIO_ADMIN_LOGIN=<root_user_login>
MINIO_ADMIN_PASSWORD=<root_user_password>

MINIO_BUCKET_NAME=<bucket_name>
MINIO_LOGIN=<backend_minio_user_login>
MINIO_PASSWORD=<backend_minio_user_password>
```
  - `minio.conf`:
```conf
MINIO_ROOT_USER="<root_user_login>"
MINIO_ROOT_PASSWORD="<root_user_passwrod>"

MINIO_VOLUMES="/mnt/minio-volume"

MINIO_OPTS="--console-address :9001"
```
3. Create folder `/mnt/minio-volume` (**this folder should be used only be MinIO**)
4. Run `docker compose up -d`

## How to start the service
1. Environment configuration
```bash
# Enter into the project directory
cd recall-back

# To create and activate virtual environment
poetry shell

# To install the defined dependencies for project
poetry install
```
2. Environment variables
  - Setpu these variables in file:
```conf
MINIO_HOSTNAME=... # <ADDR:PORT> - without protocol
MINIO_LOGIN=<backend_minio_user_login>
MINIO_PASSWORD=<backend_minio_user_login>
```
  - Activate varibles:
```bash
set -a
source <vars_file>
set +a
```
1. Run service!
```bash
# Run the service
fastapi dev app/main.py
```

### How to install `Poetry`
- https://github.com/FIT-2024-RecALL/recall-back/wiki/Poetry

## Project description

For more information about the project and its goals, please see the README, TaskBoard (Projects panel) and Issues of our organization's page.
