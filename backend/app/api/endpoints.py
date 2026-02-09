from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: str

class ChatResponse(BaseModel):
    response: str
    emotion: str
    confidence: float
    explanation: dict

from app.services.emotion import emotion_service
from app.services.memory import memory_service
from app.services.strategy import response_strategy
from app.services.explainability import explainability_service

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # 1. Detect emotion
    emotion_result = emotion_service.detect_emotion(request.message)
    top_emotion = emotion_result['top_emotion']
    confidence = emotion_result['confidence']

    # 2. Save to Memory
    memory_service.add_memory(request.user_id, request.message, top_emotion, confidence)
    
    # 3. Determine Response Strategy
    strategy = response_strategy.get_strategy(top_emotion, confidence)
    tone = strategy['tone']
    
    # 3b. Generate Response
    generated_response = response_strategy.generate_response(request.message, top_emotion, tone)

    # 4. Generate Explanation
    explanation = explainability_service.explain_decision(request.message, emotion_result)
    
    return {
        "response": generated_response,
        "emotion": top_emotion,
        "confidence": confidence,
        "explanation": {
            "tone": tone,
            "reasoning": explanation['reasoning_trace'],
            "key_tokens": explanation['key_tokens'],
            "all_scores": emotion_result['all_scores'],
            "is_sarcastic": emotion_result.get('is_sarcastic', False)
        }
    }
