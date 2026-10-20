import logging
import random
import threading

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from app.core.config import settings

logger = logging.getLogger(__name__)


class ResponseStrategy:
    def __init__(self):
        self.strategies = {
            "anger": "Calm + validation",
            "sadness": "Empathetic + supportive",
            "fear": "Reassuring + grounding",
            "joy": "Energetic + positive",
            "love": "Warm + appreciative",
            "surprise": "Curious + engaging",
            "neutral": "Polite + helpful",
        }

        self.templates = {
            "anger": ["I hear your frustration.", "Let's solve this together."],
            "sadness": ["I'm sorry you feel that way.", "I'm here for you."],
            "joy": ["That's great!", "Tell me more!"],
            "neutral": ["How can I help?", "I'm listening."],
        }

        self.generator = None
        self._generator_failed = False
        self._lock = threading.Lock()

    @property
    def is_ready(self) -> bool:
        return self.generator is not None

    def load_generator(self):
        if self.generator is not None or self._generator_failed:
            return
        with self._lock:
            if self.generator is not None or self._generator_failed:
                return
            model_name = settings.GENERATION_MODEL_NAME
            try:
                logger.info("Loading generation model: %s", model_name)
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                self.generator = pipeline(
                    "text2text-generation",
                    model=model,
                    tokenizer=tokenizer,
                )
                logger.info("Generation model loaded.")
            except Exception:
                logger.exception("Generation model unavailable; using template replies")
                self._generator_failed = True

    def get_strategy(self, emotion: str, confidence: float) -> dict:
        key = emotion if emotion in self.strategies else "neutral"
        tone = self.strategies.get(key, "Polite + helpful")
        return {"tone": tone}

    def generate_response(self, user_message: str, emotion: str, tone: str) -> str:
        self.load_generator()
        if not self.generator:
            return self._get_fallback_response(emotion)

        prompt = (
            f"Context: The user is feeling {emotion}. "
            f"Task: Reply to the user's message: '{user_message}' with a {tone} tone. "
            f"Response:"
        )

        try:
            output = self.generator(prompt, max_length=64, do_sample=True, temperature=0.7)
            return output[0]["generated_text"]
        except Exception:
            logger.exception("Generation failed")
            return self._get_fallback_response(emotion)

    def _get_fallback_response(self, emotion: str) -> str:
        key = emotion if emotion in self.templates else "neutral"
        return random.choice(self.templates.get(key, self.templates["neutral"]))


response_strategy = ResponseStrategy()
