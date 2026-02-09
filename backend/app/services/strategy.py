import logging
import random
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

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
            "neutral": "Polite + helpful"
        }
        
        # Templates as fallback
        self.templates = {
            "anger": ["I hear your frustration.", "Let's solve this together."],
            "sadness": ["I'm sorry you feel that way.", "I'm here for you."],
            "joy": ["That's great!", "Tell me more!"],
            "neutral": ["How can I help?", "I'm listening."]
        }

        # Load LLM for generation
        self.generator = None
        try:
            model_name = "google/flan-t5-small"
            logger.info(f"Loading generation model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            # Pipeline is easier for quick inference
            self.generator = pipeline("text2text-generation", model=self.model, tokenizer=self.tokenizer)
            logger.info("Generation model loaded.")
        except Exception as e:
            logger.error(f"Failed to load generation model: {e}")

    def get_strategy(self, emotion: str, confidence: float) -> dict:
        key = emotion if emotion in self.strategies else "neutral"
        tone = self.strategies.get(key, "Polite + helpful")
        return {"tone": tone}

    def generate_response(self, user_message: str, emotion: str, tone: str) -> str:
        if not self.generator:
            return self._get_fallback_response(emotion)

        # Construct Prompt
        prompt = (
            f"Context: The user is feeling {emotion}. "
            f"Task: Reply to the user's message: '{user_message}' with a {tone} tone. "
            f"Response:"
        )

        try:
            # Generate
            output = self.generator(prompt, max_length=64, do_sample=True, temperature=0.7)
            response_text = output[0]['generated_text']
            return response_text
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return self._get_fallback_response(emotion)

    def _get_fallback_response(self, emotion: str) -> str:
        key = emotion if emotion in self.templates else "neutral"
        return random.choice(self.templates.get(key, self.templates["neutral"]))

response_strategy = ResponseStrategy()
