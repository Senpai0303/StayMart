# Lightweight Production Dockerfile for StayMart Flask ML Microservice
FROM python:3.11-slim

WORKDIR /app

# Install minimal build tools for native extensions if required
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies from requirements.txt plus production WSGI server (Gunicorn)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application files and pre-trained TF-IDF models
COPY . .

ENV PORT=5000
EXPOSE 5000

# Configure Gunicorn with 1 worker and 4 threads to stay under 180MB RAM on free cloud tiers
CMD ["gunicorn", "-w", "1", "--threads", "4", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
