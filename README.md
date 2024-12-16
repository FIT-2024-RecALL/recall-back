# RecAll

## Technology Stack and Features

- [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
- [SQLAlchemy](https://https://www.sqlalchemy.org/) for the Python SQL database interactions (ORM).
- [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
- [PostgreSQL](https://www.postgresql.org) as the SQL database.
- [MinIO](https://min.io/docs/minio/linux/operations/installation.html) as S3-compatible object storage with [wrapper for Python](https://min.io/docs/minio/linux/developers/python/API.html)

## Requirements
- For deploy: [Docker Engine + Docker Compose](https://docs.docker.com/engine/install/)
- For starting the service: [Poetry](https://python-poetry.org/docs/#installation)

### How to install `Poetry`
- https://github.com/FIT-2024-RecALL/recall-back/wiki/Poetry

## Service always requires this configuration

Add config files into folder `config/` inside the root project directory:

- `auth.env`:
```conf
SECRET_KEY=<secret_key_for_encrypting>
ALGORITHM=<encrypting_algorithm: e.g. HS256>
ACCESS_TOKEN_KEY=<title_of_cookie_token_attribute>
HTTPONLY=true
SECURE=true
SAMESITE=none
```
- `minio-backend.env`:
```conf
MINIO_HOSTNAME=<minio_addr> # IP address - without protocol
MINIO_PORT=<minio_port>
MINIO_BUCKET_NAME=<bucket_name>
MINIO_LOGIN=<backend_minio_user_login>
MINIO_PASSWORD=<backend_minio_user_password>
```
- `postgres.env`:
```conf
POSTGRES_USER=<backend_postgres_user_login>
POSTGRES_PASSWORD=<backend_postgres_user_passwrod>
POSTGRES_HOST=<postgres_addr>
POSTGRES_HOST_PORT=<postgres_port>
POSTGRES_DB=<postgres_db_name>
```

## How to start the service
1. Environment configuration
```bash
cd <path_to_the_project>

poetry shell

poetry install
```
2. Run the service!
```bash
fastapi dev app/main.py

# or commercial development style
# first approach
python -m app.main
#second approach
uvicorn app.main:app --<your_flags>
```

## How to deploy

If you want to deploy service using `docker compose`, follow these instructions:
1. Download [frontend's source code](https://github.com/FIT-2024-RecALL/recall-front).
2. Create folders for MinIO object storage and Postgres DB
3. Either wrote `.env` file inside project directory with described variables:
```conf
RECALL_FRONTEND_PATH=<path_to_frontend_project_dir>
MINIO_VOLUME_PATH=<path_to_minio_storage_dir>
POSTGRES_VOLUME_PATH=<path_to_postgres_database_dir>
```
Or
> Export variables described above into your session

4. Add config file into folder `config/`:
- `minio-server.env`:
```conf
MINIO_ROOT_USER="<root_user_login>"
MINIO_ROOT_PASSWORD="<root_user_passwrod>"

MINIO_VOLUMES="/mnt/minio-volume"

MINIO_OPTS="--console-address :9001"
```

5. Run `docker compose up --build`

## Project description

For more information about the project and its goals, please see the README, TaskBoard (Projects panel) and Issues of our organization's page.
