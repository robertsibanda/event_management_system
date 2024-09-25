import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app here

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


def test_create_event(test_client):
    event_data = {
        "title": "Test Event",
        "description": "This is a test event."
    }

    response = test_client.post('/events/', json=event_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == event_data["title"]
    assert data["description"] == event_data["description"]


def test_get_all_events(test_client):
    response = test_client.get('/events/')
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    if events:
        assert "title" in events[0]
        assert "description" in events[0]


def test_get_event(test_client):
    # Assuming there is an event with id 1 in the database
    response = test_client.get('/events/1/')
    assert response.status_code == 200
    event = response.json()
    assert "title" in event
    assert "description" in event

def test_get_nonexistent_event(test_client):
    response = test_client.get('/events/9999/')
    assert response.status_code == 404
    assert response.json() == 'Event not found'


def test_update_event(test_client):
    updated_data = {
        "title": "Updated Test Event",
        "description": "Updated description."
    }

    # Assuming there is an event with id 1 in the database
    response = test_client.put('/events/1/', json=updated_data)
    assert response.status_code == 200
    updated_event = response.json()
    assert updated_event["title"] == updated_data["title"]
    assert updated_event["description"] == updated_data["description"]

def test_update_nonexistent_event(test_client):
    updated_data = {
        "title": "Nonexistent Event",
        "description": "This event does not exist."
    }

    response = test_client.put('/events/9999/', json=updated_data)
    assert response.status_code == 404