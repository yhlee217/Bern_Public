import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import logging
import time
from typing import Dict, Any
import os

from utils.config import get_settings

logger = logging.getLogger(__name__)

class SentimentModel:
    """Sentiment analysis model wrapper using Hugging Face transformers"""

    def __init__(self):
        self.settings = get_settings()
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.label_mapping = {
            'LABEL_0': 'negative',
            'LABEL_1': 'neutral',
            'LABEL_2': 'positive'
        }
        self._load_model()

    def _load_model(self):
        """Load the sentiment analysis model"""
        try:
            logger.info(f"Loading model: {self.settings.model_name}")

            # Create cache directory if it doesn't exist
            os.makedirs(self.settings.model_cache_dir, exist_ok=True)

            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.settings.model_name,
                cache_dir=self.settings.model_cache_dir
            )

            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.settings.model_name,
                cache_dir=self.settings.model_cache_dir
            )

            # Create pipeline for easier inference
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1  # Use CPU (-1), change to 0 for GPU
            )

            logger.info("Model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predict sentiment for given text

        Args:
            text: Input text to analyze

        Returns:
            Dictionary containing sentiment, confidence, and processing time
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        # Limit text length
        if len(text) > self.settings.max_text_length:
            text = text[:self.settings.max_text_length]
            logger.warning(f"Text truncated to {self.settings.max_text_length} characters")

        start_time = time.time()

        try:
            # Get prediction
            result = self.pipeline(text)[0]

            # Map label to human-readable format
            sentiment = self.label_mapping.get(result['label'], result['label'])
            if sentiment not in ['positive', 'negative', 'neutral']:
                # Fallback mapping for different model formats
                if result['label'].upper() in ['POSITIVE', 'POS']:
                    sentiment = 'positive'
                elif result['label'].upper() in ['NEGATIVE', 'NEG']:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'

            confidence = float(result['score'])
            processing_time = time.time() - start_time

            return {
                "sentiment": sentiment,
                "confidence": confidence,
                "processing_time": round(processing_time, 3)
            }

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise

    def health_check(self) -> bool:
        """Check if model is loaded and working"""
        try:
            if self.pipeline is None:
                return False

            # Test with simple text
            test_result = self.predict("This is a test")
            return test_result is not None and "sentiment" in test_result

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_name": self.settings.model_name,
            "cache_dir": self.settings.model_cache_dir,
            "max_text_length": self.settings.max_text_length,
            "device": "cpu",
            "loaded": self.pipeline is not None
        }