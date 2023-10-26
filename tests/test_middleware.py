from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv
import os
import pytest


load_dotenv()
token = os.getenv("SECRET_TOKEN")

@pytest.fixture
def client():
    return TestClient(app)

def test_valid_token(client):
    response = client.get("/get-weather/?day=2023-10-26", headers={"x-token": token})
    assert response.status_code == 200

def test_missing_token(client):
    response = client.get("/get-weather/?day=2023-10-26")
    assert response.status_code == 401

def test_invalid_token(client):
    response = client.get("/get-weather/?day=2023-10-26", headers={"x-token": "invalid-token"})
    assert response.status_code == 401
