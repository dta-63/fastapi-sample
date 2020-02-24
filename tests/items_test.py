from starlette.testclient import TestClient

from main import app

client = TestClient(app)


def test_items_routes():
    response = client.get("/items")
    assert response.status_code == 401
