from fastapi.testclient import TestClient
from entrypoints.main import app

client = TestClient(app)

def test_get_all_schedules():
    response = client.get("/schedules/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_get_schedule(monkeypatch):
    sample_schedule = {
        "id": "test123",
        "entries": [
            {"date": "12.06.2025", "hour": "1-2", "details": "Test class"}
        ]
    }

    def mock_add_schedule(doc_id, data): pass
    def mock_get_schedule(doc_id): return sample_schedule if doc_id == "test123" else None

    from app.services import firestore_service
    monkeypatch.setattr(firestore_service, "add_schedule", mock_add_schedule)
    monkeypatch.setattr(firestore_service, "get_schedule", mock_get_schedule)

    response_post = client.post("/schedules/", json=sample_schedule)
    assert response_post.status_code == 201

    response_get = client.get("/schedules/test123")
    assert response_get.status_code == 200
    assert response_get.json()["id"] == "test123"
