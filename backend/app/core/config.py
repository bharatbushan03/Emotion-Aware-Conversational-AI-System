import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Emotion-Aware Conversational AI"
    API_V1_STR: str = "/api"
    EMOTION_MODEL_NAME: str = "bhadresh-savani/bert-base-go-emotion"
    
    class Config:
        env_file = ".env"

settings = Settings()
