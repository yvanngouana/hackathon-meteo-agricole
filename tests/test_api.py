"""
Tests pour l'API FastAPI
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


class TestAPI:
    """Tests pour les endpoints API"""

    def test_root_endpoint(self):
        """Test endpoint racine"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_health_check(self):
        """Test health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    @pytest.mark.skip(reason="Nécessite clé API")
    def test_get_current_weather(self):
        """Test endpoint météo actuelle"""
        response = client.get("/api/weather/current?latitude=14.7167&longitude=-17.4677")
        assert response.status_code == 200
        assert "weather" in response.json()

    @pytest.mark.skip(reason="Nécessite clé API")
    def test_get_forecast(self):
        """Test endpoint prévisions"""
        response = client.get("/api/weather/forecast?latitude=14.7167&longitude=-17.4677&days=7")
        assert response.status_code == 200
        assert "forecasts" in response.json()
