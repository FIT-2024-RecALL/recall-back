from unittest.mock import AsyncMock

from app.schemas.user import User
from app.services.user import UserService


def test_user_registration(client, app_instance, mock_user_service):
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
    assert "id" in data
    assert "password" not in data


def test_user_login(client, app_instance, mock_user_service):
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
    assert data["nickname"] == "testuser"
    assert "id" in data


def test_user_logout(client):
    response = client.post("/user/logout")
    assert response.status_code == 200


def test_user_profile_requires_auth(client):
    response = client.get("/user/profile")
    assert response.status_code == 401


def test_user_profile_with_auth(client, app_instance, mock_user_service, auth_cookies):
    mock_user_service.get_user = AsyncMock(return_value=User(
        id=1, email="test@example.com", nickname="testuser"
    ))
    app_instance.dependency_overrides[UserService] = lambda: mock_user_service

    response = client.get("/user/profile", cookies=auth_cookies)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["email"] == "test@example.com"
