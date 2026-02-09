# Use an official Python runtime as a parent image
# Using 3.10-slim for compatibility (3.14 is too new for many ML libs in Docker)
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
# Note: We might need to adjust requirements.txt for Linux compatibility if there are win-specific libs
RUN pip install --no-cache-dir -r requirements.txt

# Install uvicorn explicitly if not in requirements
RUN pip install uvicorn

# Copy the backend code
COPY . .

# Expose the port
EXPOSE 8000

# Command to run the application
# Use shell form to allow variable expansion for $PORT (Railway requirement)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
