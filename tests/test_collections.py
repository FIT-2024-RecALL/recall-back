from unittest.mock import AsyncMock

from app.schemas.collection import Collection, CollectionShort
from app.services.collection import CollectionService


def test_create_collection_requires_auth(client):
    """POST /collections/ requires authentication."""
    response = client.post("/collections/", json={"title": "Test Collection"})
    assert response.status_code == 401


def test_get_collections(client, app_instance, mock_collection_service):
    """GET /collections/ is public (UserIdSoftDep)."""
    mock_collection_service.get_collections = AsyncMock(return_value=[
        CollectionShort(id=1, title="Collection 1", is_public=True, owner_id=1),
        CollectionShort(id=2, title="Collection 2", is_public=False, owner_id=2),
    ])
    app_instance.dependency_overrides[CollectionService] = lambda: mock_collection_service

    response = client.get("/collections/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Collection 1"
    assert data[1]["title"] == "Collection 2"


def test_get_collection_by_id(client, app_instance, mock_collection_service):
    """GET /collections/{id} works without auth for public collections."""
    mock_collection_service.get_collection = AsyncMock(return_value=Collection(
        id=1, title="Test Collection", is_public=True, owner_id=1
    ))
    app_instance.dependency_overrides[CollectionService] = lambda: mock_collection_service

    response = client.get("/collections/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Collection"
    assert data["isPublic"] is True


def test_update_collection_requires_auth(client):
    """PUT /collections/{id} requires authentication."""
    response = client.put("/collections/1", json={"title": "Updated"})
    assert response.status_code == 401


def test_delete_collection_requires_auth(client):
    """DELETE /collections/{id} requires authentication."""
    response = client.delete("/collections/1")
    assert response.status_code == 401
