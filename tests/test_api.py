# tests/test_api.py
#Test de l'api
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_observability_endpoint():
    response = client.get("/observability")
    assert response.status_code == 200
    json_data = response.json()
    # Ici tu peux tester la structure du JSON renvoyé
    assert "total_incidents" in json_data
    assert "error_rate" in json_data

