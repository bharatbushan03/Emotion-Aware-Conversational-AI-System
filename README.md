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
-   Python 3.12
-   Node.js 20+

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

## ☁️ Deploy

Deploy the API on Render first, then the frontend on Vercel. The emotion, sarcasm, and Flan-T5 models need about 4 GB of RAM. `render.yaml` selects a 2 CPU / 4 GB instance and a 5 GB disk. Render's free 512 MB plan cannot load them.

### Render (backend)

1. In the Render dashboard, choose **New** → **Blueprint** and select this repository.
2. Render reads `render.yaml` and creates `emotion-ai-api`.
3. When prompted for `ALLOWED_ORIGINS`, use `http://localhost:5173` until the Vercel URL exists, then set it to that origin (for example `https://emotion-ai.vercel.app`).
4. `GET /health` returns `models_ready: true` after the weights finish downloading. The first chat can take several minutes.

| Setting | Value |
| --- | --- |
| Root directory | `backend` |
| Build command | `bash render_build.sh` |
| Start command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health check path | `/health` |
| `PYTHON_VERSION` | `3.12.11` |
| `HF_HOME` | `/var/data/huggingface` |
| `CHROMA_DB_PATH` | `/var/data/chroma` |
| `ALLOWED_ORIGINS` | `https://<your-app>.vercel.app` |

Python is pinned to 3.12.11 because Render's default 3.14 runtime does not run this ChromaDB stack. Preview URLs on `https://*.vercel.app` are already allowed.

### Vercel (frontend)

1. Import this repository and set the root directory to `frontend`. Framework preset: Vite.
2. Before the first production build, set `VITE_API_URL` to the Render origin, such as `https://emotion-ai-api.onrender.com`. No `/api` suffix. Vite inlines this value at build time.
3. Deploy. `frontend/vercel.json` rewrites unknown paths to `index.html`.

## 🐳 Docker Deployment
Run the entire system with a single command:

```bash
docker-compose up --build -d
```
Access the app at `http://localhost:5173`.

## 📚 API Docs

Interactive API docs are at `http://localhost:8000/docs` when the backend is running.
