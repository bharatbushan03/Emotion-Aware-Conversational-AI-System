import logging
import threading

from transformers import pipeline

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmotionService:
    def __init__(self):
        self.classifier = None
        self.sarcasm_classifier = None
        self._lock = threading.Lock()

    @property
    def is_ready(self) -> bool:
        return self.classifier is not None and self.sarcasm_classifier is not None

    def load_model(self):
        if self.is_ready:
            return
        with self._lock:
            if self.is_ready:
                return
            logger.info("Loading emotion model: %s", settings.EMOTION_MODEL_NAME)
            emotion_classifier = pipeline(
                "text-classification",
                model=settings.EMOTION_MODEL_NAME,
                top_k=None,
            )
            sarcasm_classifier = pipeline(
                "text-classification",
                model=settings.SARCASM_MODEL_NAME,
                top_k=None,
            )
            self.classifier = emotion_classifier
            self.sarcasm_classifier = sarcasm_classifier
            logger.info("Emotion and sarcasm models loaded.")

    def ensure_ready(self):
        self.load_model()

    def detect_emotion(self, text: str):
        self.ensure_ready()

        results = self.classifier(text)
        emotions = results[0]
        sorted_emotions = sorted(emotions, key=lambda item: item["score"], reverse=True)
        top_emotion = sorted_emotions[0]

        sarcasm_results = self.sarcasm_classifier(text)
        sarcasm_score = next(
            (item["score"] for item in sarcasm_results[0] if item["label"] == "SARCASM"),
            0.0,
        )
        is_sarcastic = sarcasm_score > 0.5

        return {
            "top_emotion": top_emotion["label"],
            "confidence": top_emotion["score"],
            "all_scores": {item["label"]: item["score"] for item in emotions},
            "is_sarcastic": is_sarcastic,
            "sarcasm_confidence": sarcasm_score,
        }


emotion_service = EmotionService()
