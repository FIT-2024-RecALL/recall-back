import pytest
from unittest.mock import AsyncMock, Mock, patch
from contextlib import asynccontextmanager
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# App fixture (session-scoped — import once)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def app_instance():
    from app.main import app
    return app


# ---------------------------------------------------------------------------
# TestClient with mocked lifespan
# ---------------------------------------------------------------------------

@pytest.fixture
def client(app_instance):
    """TestClient that runs the full lifespan with external services mocked."""
    with (
        patch("app.main.create_db_tables", new_callable=AsyncMock),
        patch("app.main.close_db_connections", new_callable=AsyncMock),
        patch("app.main.is_bucket_available", new_callable=AsyncMock, return_value=True),
        patch("app.main.load_model", new_callable=AsyncMock, return_value="loaded"),
        patch("app.main.unload_model", new_callable=AsyncMock, return_value="unloaded"),
    ):
        with TestClient(app_instance) as c:
            yield c
    app_instance.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def auth_token():
    """Valid JWT token for user_id=1, signed with the test secret key."""
    from app.core.auth import create_access_token
    return create_access_token(user_id=1)


@pytest.fixture(scope="session")
def auth_cookies(auth_token):
    from app.core.config import get_settings
    return {get_settings().access_token_key: auth_token}


# ---------------------------------------------------------------------------
# Mock Unit-of-Work (for unit tests that test service logic directly)
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_uow():
    mock = Mock()

    @asynccontextmanager
    async def mock_begin():
        yield mock

    mock.begin = mock_begin
    return mock


# ---------------------------------------------------------------------------
# Generic service mocks (used by API tests via dependency_overrides)
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_user_service():
    return Mock()


@pytest.fixture
def mock_card_service():
    return Mock()


@pytest.fixture
def mock_collection_service():
    return Mock()
