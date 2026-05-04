from fastapi.testclient import TestClient

import app.api.endpoints as endpoints
from app.main import app


class DummyEmotionService:
    def detect_emotion(self, text: str):
        return {
            "top_emotion": "joy",
            "confidence": 0.95,
            "all_scores": {"joy": 0.95, "sadness": 0.02},
            "is_sarcastic": False,
        }


class DummyMemoryService:
    def add_memory(self, user_id, text, emotion, confidence):
        # noop for test
        return None


class DummyStrategy:
    def get_strategy(self, emotion, confidence):
        return {"tone": "Energetic + positive"}

    def generate_response(self, user_message, emotion, tone):
        return f"(mock reply to '{user_message}')"


class DummyExplainability:
    def explain_decision(self, text, emotion_result):
        return {
            "reasoning_trace": "High joy detected based on positive phrasing.",
            "key_tokens": ["great", "happy"],
            "model_confidence": emotion_result["confidence"] if "confidence" in emotion_result else 0.95,
        }


def test_chat_endpoint_monkeypatched():
    # Monkeypatch the service instances used by the endpoint module
    endpoints.emotion_service = DummyEmotionService()
    endpoints.memory_service = DummyMemoryService()
    endpoints.response_strategy = DummyStrategy()
    endpoints.explainability_service = DummyExplainability()

    client = TestClient(app)

    payload = {"message": "This is great news!", "user_id": "unit_test_user"}
    r = client.post("/api/chat", json=payload)
    assert r.status_code == 200
    body = r.json()

    assert "response" in body
    assert body["emotion"] == "joy"
    assert body["confidence"] >= 0.9
    assert "explanation" in body
    assert body["explanation"]["tone"] == "Energetic + positive"
