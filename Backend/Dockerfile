# Lightweight Python runtime for the FastAPI backend.
FROM python:3.11-slim

# Backend application files live in /app inside the container.
WORKDIR /app

# Install Python packages first so this Docker layer can be cached.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the FastAPI source code.
COPY . .

# FastAPI listens on port 4000.
EXPOSE 4000

# Start Uvicorn and bind to all interfaces so Docker can expose the port.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]
