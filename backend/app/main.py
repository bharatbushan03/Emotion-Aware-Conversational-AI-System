from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints

app = FastAPI(
    title="Emotion-Aware Conversational AI",
    description="Backend API for Emotion-Aware Conversational AI System",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(endpoints.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Emotion-Aware AI Backend is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
