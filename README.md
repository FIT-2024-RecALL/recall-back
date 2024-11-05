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
- Set env variable `RECALL_PROJECT_PATH` to project dir
- Add config files into `minio_config/`:
  - `minio-backend.env`:
```conf
MINIO_HOSTNAME=... # <ADDR:PORT> - without protocol
MINIO_BUCKET_NAME=<bucket_name>
MINIO_LOGIN=<backend_minio_user_login>
MINIO_PASSWORD=<backend_minio_user_password>
```
  - `minio-server.env`:
```conf
MINIO_ROOT_USER="<root_user_login>"
MINIO_ROOT_PASSWORD="<root_user_passwrod>"

MINIO_VOLUMES="/mnt/minio-volume"

MINIO_OPTS="--console-address :9001"
```
- Create folder for MinIO object storage and set its path to env var `MINIO_VOLUME_PATH`
- Run `docker compose up -d`

## How to start the service
1. Environment configuration
```bash
cd $RECALL_PROJECT_PATH

poetry shell

poetry install
```
2. Activate next files with env vars: `./config/minio-backend.env`
```bash
set -a
source <vars_files>
# ...
set +a
```
3. Run service!
```bash
fastapi dev app/main.py
```

### How to install `Poetry`
- https://github.com/FIT-2024-RecALL/recall-back/wiki/Poetry

## Project description

For more information about the project and its goals, please see the README, TaskBoard (Projects panel) and Issues of our organization's page.
