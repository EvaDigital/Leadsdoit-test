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

def test_valid_day(client):
    response = client.get("/get-weather/?day=2023-10-26", headers={"x-token": token})
    assert response.status_code == 200

def test_missing_day(client):
    response = client.get("/get-weather/", headers={"x-token": token})
    assert response.status_code == 400

def test_invalid_day(client):
    response = client.get("/get-weather/?day=10-12-2023", headers={"x-token": token})
    assert response.status_code == 400
