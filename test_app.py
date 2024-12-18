import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_predict_train_file(client):
    response = client.post('/predict', json={"file": "train"})
    assert response.status_code == 200
    assert "average_price" in response.json

def test_predict_invalid_file(client):
    response = client.post('/predict', json={"file": "invalid"})
    assert response.status_code == 200
    assert "error" in response.json

def test_predict_test_file(client):
    response = client.post('/predict', json={"file": "test"})
    assert response.status_code == 200
    assert "message" in response.json or "average_price" in response.json
