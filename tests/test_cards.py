from unittest.mock import AsyncMock

from app.schemas.card import Card
from app.services.card import CardService


def test_create_card_requires_auth(client):
    """POST /cards/ requires authentication."""
    response = client.post("/cards/", json={
        "frontSide": "Front of card",
        "backSide": "Back of card"
    })
    assert response.status_code == 401


def test_get_card_by_id(client, app_instance, mock_card_service):
    """GET /cards/{id} works without auth (UserIdSoftDep)."""
    mock_card_service.get_card = AsyncMock(return_value=Card(
        id=1, front_side="Front of card", back_side="Back of card",
        owner_id=1, is_public=True
    ))
    app_instance.dependency_overrides[CardService] = lambda: mock_card_service

    response = client.get("/cards/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["frontSide"] == "Front of card"
    assert data["backSide"] == "Back of card"


def test_update_card_requires_auth(client):
    """PUT /cards/{id} requires authentication."""
    response = client.put("/cards/1", json={
        "frontSide": "Updated front",
        "backSide": "Updated back"
    })
    assert response.status_code == 401


def test_delete_card_requires_auth(client):
    """DELETE /cards/{id} requires authentication."""
    response = client.delete("/cards/1")
    assert response.status_code == 401
