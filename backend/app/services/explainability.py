import logging

logger = logging.getLogger(__name__)

class ExplainabilityService:
    def __init__(self):
        pass

    def explain_decision(self, text: str, emotion_result: dict) -> dict:
        """
        Generates an explanation for the detected emotion.
        In a real system, this would use SHAP or Integrated Gradients.
        Here we use a heuristic approach based on keywords and scores.
        """
        top_emotion = emotion_result['top_emotion']
        confidence = emotion_result['confidence']
        
        # Mock reasoning
        reasoning = f"The model detected '{top_emotion}' with {confidence:.2f} confidence."
        
        if confidence > 0.8:
            reasoning += " The emotional cues were very strong."
        elif confidence > 0.5:
            reasoning += " There were moderate emotional indicators."
        else:
            reasoning += " The emotion was subtle and difficult to classify with certainty."

        # Simple keyword highlighting (mock)
        # In production, use attention weights
        words = text.split()
        key_tokens = [w for w in words if len(w) > 4] # Mock heuristic
        
        return {
            "reasoning_trace": reasoning,
            "key_tokens": key_tokens[:3], # Top 3 "influential" words
            "model_confidence": confidence
        }

explainability_service = ExplainabilityService()
