from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_others_routes():
    response = client.get("/others?required=test")
    assert response.status_code == 200
    assert response.json() == [{"id": "5df9e0fecdd49b0030b58622", "test": "Test 1"}]