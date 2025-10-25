import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.sentiment_model import SentimentModel

class TestSentimentModel:
    """Test sentiment model class"""

    @patch('models.sentiment_model.AutoTokenizer')
    @patch('models.sentiment_model.AutoModelForSequenceClassification')
    @patch('models.sentiment_model.pipeline')
    def test_model_initialization(self, mock_pipeline, mock_model, mock_tokenizer):
        """Test model initialization"""
        # Mock the pipeline
        mock_pipeline_instance = Mock()
        mock_pipeline.return_value = mock_pipeline_instance

        # Initialize model
        model = SentimentModel()

        # Verify model is loaded
        assert model.pipeline is not None
        mock_tokenizer.from_pretrained.assert_called_once()
        mock_model.from_pretrained.assert_called_once()

    @patch('models.sentiment_model.AutoTokenizer')
    @patch('models.sentiment_model.AutoModelForSequenceClassification')
    @patch('models.sentiment_model.pipeline')
    def test_predict_success(self, mock_pipeline, mock_model, mock_tokenizer):
        """Test successful prediction"""
        # Mock pipeline result
        mock_pipeline_instance = Mock()
        mock_pipeline_instance.return_value = [{
            'label': 'LABEL_2',
            'score': 0.95
        }]
        mock_pipeline.return_value = mock_pipeline_instance

        # Initialize model and predict
        model = SentimentModel()
        result = model.predict("I love this!")

        # Verify result
        assert result["sentiment"] == "positive"
        assert result["confidence"] == 0.95
        assert "processing_time" in result

    @patch('models.sentiment_model.AutoTokenizer')
    @patch('models.sentiment_model.AutoModelForSequenceClassification')
    @patch('models.sentiment_model.pipeline')
    def test_predict_negative_sentiment(self, mock_pipeline, mock_model, mock_tokenizer):
        """Test negative sentiment prediction"""
        mock_pipeline_instance = Mock()
        mock_pipeline_instance.return_value = [{
            'label': 'LABEL_0',
            'score': 0.85
        }]
        mock_pipeline.return_value = mock_pipeline_instance

        model = SentimentModel()
        result = model.predict("I hate this!")

        assert result["sentiment"] == "negative"
        assert result["confidence"] == 0.85

    @patch('models.sentiment_model.AutoTokenizer')
    @patch('models.sentiment_model.AutoModelForSequenceClassification')
    @patch('models.sentiment_model.pipeline')
    def test_predict_neutral_sentiment(self, mock_pipeline, mock_model, mock_tokenizer):
        """Test neutral sentiment prediction"""
        mock_pipeline_instance = Mock()
        mock_pipeline_instance.return_value = [{
            'label': 'LABEL_1',
            'score': 0.75
        }]
        mock_pipeline.return_value = mock_pipeline_instance

        model = SentimentModel()
        result = model.predict("This is okay.")

        assert result["sentiment"] == "neutral"
        assert result["confidence"] == 0.75

    @patch('models.sentiment_model.AutoTokenizer')
    @patch('models.sentiment_model.AutoModelForSequenceClassification')
    @patch('models.sentiment_model.pipeline')
    def test_predict_empty_text(self, mock_pipeline, mock_model, mock_tokenizer):
        """Test prediction with empty text"""
        mock_pipeline.return_value = Mock()

        model = SentimentModel()

        with pytest.raises(ValueError, match="Input text cannot be empty"):
            model.predict("")

        with pytest.raises(ValueError, match="Input text cannot be empty"):
            model.predict("   ")

    @patch('models.sentiment_model.AutoTokenizer')
    @patch('models.sentiment_model.AutoModelForSequenceClassification')
    @patch('models.sentiment_model.pipeline')
    def test_predict_long_text(self, mock_pipeline, mock_model, mock_tokenizer):
        """Test prediction with long text (should be truncated)"""
        mock_pipeline_instance = Mock()
        mock_pipeline_instance.return_value = [{
            'label': 'LABEL_2',
            'score': 0.90
        }]
        mock_pipeline.return_value = mock_pipeline_instance

        model = SentimentModel()
        long_text = "a" * 1000  # Longer than max_length

        result = model.predict(long_text)

        # Should still work (text gets truncated)
        assert result["sentiment"] == "positive"
        assert result["confidence"] == 0.90

    @patch('models.sentiment_model.AutoTokenizer')
    @patch('models.sentiment_model.AutoModelForSequenceClassification')
    @patch('models.sentiment_model.pipeline')
    def test_health_check_success(self, mock_pipeline, mock_model, mock_tokenizer):
        """Test successful health check"""
        mock_pipeline_instance = Mock()
        mock_pipeline_instance.return_value = [{
            'label': 'LABEL_2',
            'score': 0.95
        }]
        mock_pipeline.return_value = mock_pipeline_instance

        model = SentimentModel()
        is_healthy = model.health_check()

        assert is_healthy is True

    @patch('models.sentiment_model.AutoTokenizer')
    @patch('models.sentiment_model.AutoModelForSequenceClassification')
    @patch('models.sentiment_model.pipeline')
    def test_health_check_failure(self, mock_pipeline, mock_model, mock_tokenizer):
        """Test health check when model is not working"""
        mock_pipeline_instance = Mock()
        mock_pipeline_instance.side_effect = Exception("Model error")
        mock_pipeline.return_value = mock_pipeline_instance

        model = SentimentModel()
        is_healthy = model.health_check()

        assert is_healthy is False

    @patch('models.sentiment_model.AutoTokenizer')
    @patch('models.sentiment_model.AutoModelForSequenceClassification')
    @patch('models.sentiment_model.pipeline')
    def test_get_model_info(self, mock_pipeline, mock_model, mock_tokenizer):
        """Test getting model information"""
        mock_pipeline.return_value = Mock()

        model = SentimentModel()
        info = model.get_model_info()

        assert "model_name" in info
        assert "cache_dir" in info
        assert "max_text_length" in info
        assert "device" in info
        assert "loaded" in info

if __name__ == "__main__":
    pytest.main([__file__])