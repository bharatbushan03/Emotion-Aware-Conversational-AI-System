# Deployment Guide

## Local Development

### Backend
1. Open a terminal in the repository root.
2. Run `run_backend.bat` on Windows or activate `backend/venv` manually.
3. Start the API with:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

The backend runs on `http://localhost:8000`.

### Frontend
1. Open a second terminal in the repository root.
2. Run `run_frontend.bat` on Windows or start Vite manually.

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173`.

## Docker Deployment
Use Docker Compose to start both services together:

```bash
docker compose up --build
```

If you prefer detached mode:

```bash
docker compose up --build -d
```

## Environment Notes
- Set `VITE_API_URL` in the frontend if the backend is not on `http://localhost:8000`.
- The backend currently uses the bundled model names in `backend/app/core/config.py`.
- ChromaDB persistence is mounted through the `chroma_data` volume in `docker-compose.yml`.