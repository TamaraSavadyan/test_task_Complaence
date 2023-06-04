import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.models import User

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_create_user(client, db_session):
    request = {
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com"
    }
    response = await client.post('/register', json=request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['username'] == "testuser"

    created_user = db_session.query(User).filter(User.username == "testuser").first()
    assert created_user is not None
    assert created_user.email == "test@example.com"

    db_session.query(User).delete()
    db_session.commit()
