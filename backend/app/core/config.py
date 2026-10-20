from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Emotion-Aware Conversational AI"
    API_V1_STR: str = "/api"
    EMOTION_MODEL_NAME: str = "bhadresh-savani/bert-base-go-emotion"
    SARCASM_MODEL_NAME: str = "helinivan/english-sarcasm-detector"
    GENERATION_MODEL_NAME: str = "google/flan-t5-small"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    CORS_ORIGIN_REGEX: str = r"https://.*\.vercel\.app"
    CHROMA_DB_PATH: str = "./chroma_db_storage"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
