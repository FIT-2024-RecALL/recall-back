from fastapi.testclient import TestClient
from app.main import app


def test_app_startup():
    """Test that the app starts up successfully"""
    # This test just verifies that the app can be imported and initialized
    assert app is not None


def test_read_main():
    """Test the root endpoint"""
    client = TestClient(app)
    response = client.get("/")
    # The app now has a root endpoint
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to RecAll API"}