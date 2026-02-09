@echo off
echo Starting Backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    pip install uvicorn
) else (
    call venv\Scripts\activate
)

echo Running Uvicorn...
python -m uvicorn app.main:app --reload
pause
