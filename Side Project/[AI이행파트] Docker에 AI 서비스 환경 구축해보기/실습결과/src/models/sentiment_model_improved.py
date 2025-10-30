"""
개선된 감정분석 모델 (한글 지원)

문제점: 기존 cardiffnlp/twitter-roberta-base-sentiment-latest 모델은 영어 전용
해결책: 다국어 지원 모델로 변경

추천 모델:
1. nlptown/bert-base-multilingual-uncased-sentiment (다국어, 별점 5단계)
2. cardiffnlp/twitter-xlm-roberta-base-sentiment (다국어, 3단계)
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import logging
import time
from typing import Dict, Any
import os

from utils.config import get_settings

logger = logging.getLogger(__name__)

class SentimentModelImproved:
    """개선된 감정분석 모델 (한글 지원)"""

    def __init__(self, use_multilingual=True):
        """
        Args:
            use_multilingual: True면 다국어 모델 사용, False면 영어 전용 모델 사용
        """
        self.settings = get_settings()
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.use_multilingual = use_multilingual

        # 다국어 모델 사용 시 모델명 변경
        if use_multilingual:
            # Option 1: 별점 5단계 모델 (한글 잘 지원)
            self.model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
            self.label_mapping = {
                '1 star': 'negative',   # 매우 부정
                '2 stars': 'negative',  # 부정
                '3 stars': 'neutral',   # 중립
                '4 stars': 'positive',  # 긍정
                '5 stars': 'positive'   # 매우 긍정
            }

            # Option 2: 3단계 다국어 모델 (Twitter 기반)
            # self.model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
            # self.label_mapping = {
            #     'LABEL_0': 'negative',
            #     'LABEL_1': 'neutral',
            #     'LABEL_2': 'positive'
            # }
        else:
            # 영어 전용 모델
            self.model_name = self.settings.model_name
            self.label_mapping = {
                'LABEL_0': 'negative',
                'LABEL_1': 'neutral',
                'LABEL_2': 'positive'
            }

        self._load_model()

    def _load_model(self):
        """모델 로딩"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            logger.info(f"Multilingual mode: {self.use_multilingual}")

            # 캐시 디렉토리 생성
            os.makedirs(self.settings.model_cache_dir, exist_ok=True)

            # 토크나이저 및 모델 로드
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.settings.model_cache_dir
            )

            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                cache_dir=self.settings.model_cache_dir
            )

            # Pipeline 생성
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1  # CPU 사용 (-1), GPU는 0
            )

            logger.info("Model loaded successfully")
            logger.info(f"Model supports: {'한글/영어/다국어' if self.use_multilingual else '영어만'}")

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def predict(self, text: str) -> Dict[str, Any]:
        """
        텍스트 감정 예측

        Args:
            text: 분석할 텍스트 (한글/영어 모두 가능)

        Returns:
            {
                "sentiment": "positive/negative/neutral",
                "confidence": 0.95,
                "processing_time": 0.123,
                "raw_label": "5 stars",  # 원본 레이블
                "model": "multilingual" or "english-only"
            }
        """
        if not text or not text.strip():
            raise ValueError("입력 텍스트가 비어있습니다")

        # 텍스트 길이 제한
        if len(text) > self.settings.max_text_length:
            text = text[:self.settings.max_text_length]
            logger.warning(f"텍스트가 {self.settings.max_text_length}자로 잘렸습니다")

        start_time = time.time()

        try:
            # 예측 실행
            result = self.pipeline(text)[0]

            # 레이블 매핑
            raw_label = result['label']
            sentiment = self.label_mapping.get(raw_label, 'neutral')

            # 별점 모델의 경우 신뢰도 조정
            confidence = float(result['score'])

            processing_time = time.time() - start_time

            return {
                "sentiment": sentiment,
                "confidence": round(confidence, 4),
                "processing_time": round(processing_time, 3),
                "raw_label": raw_label,
                "model": "multilingual" if self.use_multilingual else "english-only"
            }

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise

    def predict_with_scores(self, text: str) -> Dict[str, Any]:
        """
        모든 감정 점수 반환 (별점 모델용)

        Returns:
            {
                "sentiment": "positive",
                "scores": {
                    "negative": 0.05,
                    "neutral": 0.15,
                    "positive": 0.80
                },
                "confidence": 0.80,
                "raw_scores": [...],  # 원본 별점 점수
                "processing_time": 0.123
            }
        """
        if not text or not text.strip():
            raise ValueError("입력 텍스트가 비어있습니다")

        start_time = time.time()

        try:
            # 모든 레이블의 점수 가져오기
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

            with torch.no_grad():
                outputs = self.model(**inputs)
                scores = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]

            # 점수를 감정별로 그룹화
            sentiment_scores = {
                'negative': 0.0,
                'neutral': 0.0,
                'positive': 0.0
            }

            raw_scores = {}
            for idx, score in enumerate(scores):
                # 모델의 id2label 매핑 사용
                label = self.model.config.id2label.get(idx, f'LABEL_{idx}')
                raw_scores[label] = float(score)

                # 감정 카테고리로 매핑
                mapped_sentiment = self.label_mapping.get(label, 'neutral')
                sentiment_scores[mapped_sentiment] += float(score)

            # 가장 높은 점수의 감정 선택
            sentiment = max(sentiment_scores, key=sentiment_scores.get)
            confidence = sentiment_scores[sentiment]

            processing_time = time.time() - start_time

            return {
                "sentiment": sentiment,
                "scores": {k: round(v, 4) for k, v in sentiment_scores.items()},
                "confidence": round(confidence, 4),
                "raw_scores": {k: round(v, 4) for k, v in raw_scores.items()},
                "processing_time": round(processing_time, 3),
                "model": "multilingual" if self.use_multilingual else "english-only"
            }

        except Exception as e:
            logger.error(f"Detailed prediction failed: {e}")
            raise

    def health_check(self) -> bool:
        """모델 정상 작동 확인"""
        try:
            if self.pipeline is None:
                return False

            # 한글과 영어 모두 테스트
            test_result_ko = self.predict("좋은 하루")
            test_result_en = self.predict("Good day")

            return (test_result_ko is not None and
                    test_result_en is not None and
                    "sentiment" in test_result_ko)

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """모델 정보 반환"""
        return {
            "model_name": self.model_name,
            "model_type": "multilingual" if self.use_multilingual else "english-only",
            "supported_languages": "한국어, 영어, 중국어, 일본어 등 100+ 언어" if self.use_multilingual else "영어만",
            "cache_dir": self.settings.model_cache_dir,
            "max_text_length": self.settings.max_text_length,
            "device": "cpu",
            "loaded": self.pipeline is not None,
            "label_mapping": self.label_mapping
        }


# 기존 코드와의 호환성을 위한 별칭
SentimentModel = SentimentModelImproved
