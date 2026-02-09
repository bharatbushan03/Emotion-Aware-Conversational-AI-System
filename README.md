# Emotion-Aware Conversational AI System

## 🌟 Overview
This is a production-grade **Emotion-Aware Conversational AI System** capable of detecting human emotions in real-time, maintaining emotional context across conversations, and generating adaptive, empathetic responses using a local LLM.

## ✨ Key Features
-   **Real-time Emotion Detection**: Uses `RoBERTa` (via Hugging Face) to detect 27+ emotions (Joy, Sadness, Anger, etc.).
-   **Adaptive Response Generation**: Integrated **Google Flan-T5** LLM to generate unique, context-aware responses based on the user's emotional state.
-   **Emotional Memory**: Tracks user emotion history using **ChromaDB** (with in-memory fallback) to maintain context.
-   **Explainability**: Provides reasoning traces and confidence scores for every detection.
-   **Modern UI**: React + TypeScript frontend with real-time emotion dashboard.
-   **Docker Ready**: Full containerization for easy deployment.

## 🛠️ Tech Stack
-   **Backend**: Python, FastAPI, PyTorch, Transformers, ChromaDB.
-   **Frontend**: React, TypeScript, Vite.
-   **AI Models**:
    -   Emotion: `bhadresh-savani/bert-base-go-emotion`
    -   Generation: `google/flan-t5-small`
-   **DevOps**: Docker, Docker Compose.

## 🚀 Quick Start (Local)

### Prerequisites
-   Python 3.10+
-   Node.js 18+

### 1. Backend (FastAPI)
```bash
# Windows (using helper script)
./run_backend.bat

# Manual Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
*Port: `8000`*

### 2. Frontend (React)
```bash
# Windows (using helper script)
./run_frontend.bat

# Manual Setup
cd frontend
npm install
npm run dev
```
*Port: `5173`*

## 🐳 Docker Deployment
Run the entire system with a single command:

```bash
docker-compose up --build -d
```
Access the app at `http://localhost:5173`.

## 📚 Documentation
-   [Implementation Plan](implementation_plan.md)
-   [Deployment Guide](deployment_guide.md)
-   [API Docs](http://localhost:8000/docs)
