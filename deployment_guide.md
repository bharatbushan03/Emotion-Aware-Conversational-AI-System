# Deployment Guide

The frontend is a static Vite app for Vercel. The API is a FastAPI service for Render. Deploy the API first so you have its public URL for the frontend build.

The emotion, sarcasm, and Flan-T5 models need about 4 GB of RAM. Render's free 512 MB instance cannot load them. `render.yaml` selects a 2 CPU / 4 GB web service and a 5 GB disk for the model cache and ChromaDB.

## Render (backend)

1. Push this repository to GitHub.
2. In the Render dashboard, choose **New** → **Blueprint** and select the repository.
3. Render reads `render.yaml` and creates a web service named `emotion-ai-api`.
4. When prompted for `ALLOWED_ORIGINS`, enter the Vercel URL after the frontend exists. For the first deploy you can use `http://localhost:5173` and update it later.
5. Wait until the service is live. The first chat request downloads the models onto the disk, so it can take several minutes. `GET /health` returns `models_ready: true` when loading has finished.

The service listens on `0.0.0.0:$PORT`. Python is pinned to 3.12.11 because Render's default 3.14 build does not run this ChromaDB stack. PyTorch is the CPU wheel from `requirements.txt`.

Useful values:

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

Preview URLs on `https://*.vercel.app` are already allowed by `CORS_ORIGIN_REGEX`. A custom domain has to be added to `ALLOWED_ORIGINS`.

Manual setup uses the same root directory, build command, start command, plan (`2c-4g`), and disk mount (`/var/data`, 5 GB).

## Vercel (frontend)

1. Import the same GitHub repository as a Vercel project.
2. Set the project **Root Directory** to `frontend`. Framework preset: Vite.
3. Add an environment variable before the first production build:

```
VITE_API_URL=https://emotion-ai-api.onrender.com
```

Use the real Render URL, with `https://` and no `/api` suffix. Vite inlines this value at build time, so change it and redeploy when the API URL changes.

4. Deploy. `frontend/vercel.json` rewrites unknown paths to `index.html`.

After the Vercel URL exists, set Render's `ALLOWED_ORIGINS` to that origin (for example `https://emotion-ai.vercel.app`) and redeploy the API if it is already running.

## Local development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API listens on `http://localhost:8000`. On Windows, `run_backend.bat` does the same setup.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI listens on `http://localhost:5173`. Copy `frontend/.env.example` to `frontend/.env` only if the API is not on `http://localhost:8000`.

## Docker

```bash
docker compose up --build
```

The Compose stack is for local containers. Vercel and Render use the native builds described above.
