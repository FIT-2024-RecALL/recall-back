# RecAll

## Technology Stack and Features

- [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
- [SQLAlchemy](https://https://www.sqlalchemy.org/) for the Python SQL database interactions (ORM).
- [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
- [PostgreSQL](https://www.postgresql.org) as the SQL database.

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
MINIO_LOGIN=...
MINIO_PASSWORD=...
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
