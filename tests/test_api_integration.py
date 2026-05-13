"""
Integration smoke tests that verify routing and auth enforcement end-to-end.
All external services (DB, Minio, Ollama) are mocked via conftest `client`.
"""
from unittest.mock import AsyncMock

from app.schemas.user import User
from app.services.user import UserService


# ---------------------------------------------------------------------------
# Health / Root
# ---------------------------------------------------------------------------

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to RecAll API"}


# ---------------------------------------------------------------------------
# User registration & login (services mocked via dependency_overrides)
# ---------------------------------------------------------------------------

def test_user_registration_integration(client, app_instance, mock_user_service):
    mock_user_service.register_user = AsyncMock(return_value=User(
        id=1, email="test@example.com", nickname="testuser"
    ))
    app_instance.dependency_overrides[UserService] = lambda: mock_user_service

    response = client.post("/user/register", json={
        "email": "test@example.com",
        "nickname": "testuser",
        "password": "testpassword123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["nickname"] == "testuser"
    assert data["id"] == 1
    assert "password" not in data


def test_user_login_integration(client, app_instance, mock_user_service):
    mock_user_service.authenticate_user = AsyncMock(return_value=User(
        id=1, email="test@example.com", nickname="testuser"
    ))
    app_instance.dependency_overrides[UserService] = lambda: mock_user_service

    response = client.post("/user/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["id"] == 1


def test_user_logout_integration(client):
    response = client.post("/user/logout")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Auth enforcement
# ---------------------------------------------------------------------------

def test_create_card_requires_auth(client):
    response = client.post("/cards/", json={"frontSide": "Q", "backSide": "A"})
    assert response.status_code == 401


def test_create_collection_requires_auth(client):
    response = client.post("/collections/", json={"title": "My Collection"})
    assert response.status_code == 401
