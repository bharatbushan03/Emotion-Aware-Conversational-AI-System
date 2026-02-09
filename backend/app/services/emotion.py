from transformers import pipeline
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmotionService:
    def __init__(self):
        self.classifier = None
        self.load_model()

    def load_model(self):
        try:
            logger.info(f"Loading emotion model: {settings.EMOTION_MODEL_NAME}")
            self.classifier = pipeline(
                "text-classification",
                model=settings.EMOTION_MODEL_NAME,
                return_all_scores=True
            )
            # Sarcasm detection
            self.sarcasm_classifier = pipeline(
                "text-classification",
                model="helinivan/english-sarcasm-detector",
                return_all_scores=True
            )
            logger.info("Emotion and Sarcasm models loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise e

    def detect_emotion(self, text: str):
        if not self.classifier:
            self.load_model()
        
        # Emotion detection
        results = self.classifier(text)
        emotions = results[0]
        sorted_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)
        top_emotion = sorted_emotions[0]
        
        # Sarcasm detection
        sarcasm_results = self.sarcasm_classifier(text) # [{'label': 'SARCASM', 'score': 0.9}, ...]
        sarcasm_score = next((r['score'] for r in sarcasm_results[0] if r['label'] == 'SARCASM'), 0.0)
        is_sarcastic = sarcasm_score > 0.5

        return {
            "top_emotion": top_emotion['label'],
            "confidence": top_emotion['score'],
            "all_scores": {e['label']: e['score'] for e in emotions},
            "is_sarcastic": is_sarcastic,
            "sarcasm_confidence": sarcasm_score
        }

emotion_service = EmotionService()
