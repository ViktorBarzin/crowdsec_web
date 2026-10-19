# ---- Stage 1: Build dependencies ----
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Copy requirement files
COPY requirements.txt .

# Install to a local folder
RUN pip install --prefix=/install -r requirements.txt

# ---- Stage 2: Runtime ----
FROM python:3.12-slim

WORKDIR /app

# Pull Debian security fixes the base image has not picked up yet.
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy app source
COPY app ./app

# Create non-root user
RUN useradd -m fastapiuser && chown -R fastapiuser /app
USER fastapiuser

# Expose FastAPI port
EXPOSE 8000

# Start app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
