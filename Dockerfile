FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements first for better caching
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy root requirements (if needed or for completeness)
COPY requirements.txt .

# Copy the backend source code
COPY backend/ ./backend/

# Set working directory to backend so main:app can be found and imports work
WORKDIR /app/backend

# Use port 10000 which is common for Render
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
