import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app
from models.sentiment_model import SentimentModel

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture
def mock_model():
    """Mock sentiment model fixture"""
    model = Mock(spec=SentimentModel)
    model.predict.return_value = {
        "sentiment": "positive",
        "confidence": 0.95,
        "processing_time": 0.12
    }
    model.health_check.return_value = True
    model.get_model_info.return_value = {
        "model_name": "test-model",
        "cache_dir": "./test/cache",
        "max_text_length": 512,
        "device": "cpu",
        "loaded": True
    }
    return model

class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check_success(self, client):
        """Test successful health check"""
        with patch('main.model_instance') as mock_instance:
            mock_instance.return_value = Mock()
            response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "model_loaded" in data

    def test_health_check_model_not_loaded(self, client):
        """Test health check when model is not loaded"""
        with patch('main.model_instance', None):
            response = client.get("/health")

        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["model_loaded"] is False

class TestRootEndpoint:
    """Test root endpoint"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns correct information"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data

class TestPredictEndpoint:
    """Test prediction endpoint"""

    @patch('main.get_model')
    def test_predict_success(self, mock_get_model, client, mock_model):
        """Test successful prediction"""
        mock_get_model.return_value = mock_model

        response = client.post(
            "/predict",
            json={"text": "I love this product!"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] == "positive"
        assert data["confidence"] == 0.95
        assert data["processing_time"] == 0.12

    def test_predict_empty_text(self, client):
        """Test prediction with empty text"""
        response = client.post(
            "/predict",
            json={"text": ""}
        )

        assert response.status_code == 422  # Validation error

    def test_predict_missing_text(self, client):
        """Test prediction with missing text field"""
        response = client.post(
            "/predict",
            json={}
        )

        assert response.status_code == 422  # Validation error

    def test_predict_long_text(self, client):
        """Test prediction with very long text"""
        long_text = "a" * 1000  # Longer than max_length

        response = client.post(
            "/predict",
            json={"text": long_text}
        )

        # Should still process (truncated) or return validation error
        assert response.status_code in [200, 422]

class TestModelEndpoints:
    """Test model-related endpoints"""

    @patch('main.get_model')
    def test_model_info(self, mock_get_model, client, mock_model):
        """Test model info endpoint"""
        mock_get_model.return_value = mock_model

        response = client.get("/model/info")

        assert response.status_code == 200
        data = response.json()
        assert "model_name" in data
        assert "loaded" in data

    @patch('main.get_model')
    def test_model_health(self, mock_get_model, client, mock_model):
        """Test model health endpoint"""
        mock_get_model.return_value = mock_model

        response = client.post("/model/health")

        assert response.status_code == 200
        data = response.json()
        assert "model_healthy" in data
        assert "status" in data

if __name__ == "__main__":
    pytest.main([__file__])