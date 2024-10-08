# RecAll

## Technology Stack and Features

- [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
- [SQLAlchemy](https://https://www.sqlalchemy.org/) for the Python SQL database interactions (ORM).
- [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
- [PostgreSQL](https://www.postgresql.org) as the SQL database.

## How to start the service

```bash
# Enter into the project directory
cd recall-back

# To create a virtual environment, you can use the venv module that comes with Python
python -m venv .venv

# Activate the new virtual environment
# On Windows PowerShell, run
.venv\Scripts\activate
# Upgrade pip
python -m pip install --upgrade pip

# Install packages from requirements.txt
pip install -r requirements.txt

# Run the service
fastapi dev app/main.py
```

## Project description

For more information about the project and its goals, please see the README, TaskBoard (Projects panel) and Issues of our organization's page.
