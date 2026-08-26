from fastapi.testclient import TestClient

from app.main import app


# Create a test client for our FastAPI application
client = TestClient(app)


# Test the home route
def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to TaskFlow API"


# Test creating a user
def test_create_user():
    response = client.post(
        "/users/",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "12345"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Test User"


# Test getting all users
def test_get_users():
    response = client.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test getting a user that does not exist
def test_get_user_not_found():
    response = client.get("/users/99999")

    assert response.status_code == 404


# Test creating a task
def test_create_task():
    response = client.post(
        "/tasks/",
        json={
            "title": "Learn FastAPI",
            "description": "Practice FastAPI testing",
            "status": "pending",
            "user_id": 1
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Learn FastAPI"


# Test getting all tasks
def test_get_tasks():
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test getting a task that does not exist
def test_get_task_not_found():
    response = client.get("/tasks/99999")

    assert response.status_code == 404