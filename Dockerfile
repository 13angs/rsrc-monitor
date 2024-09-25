FROM python:3.12-slim

# Install PostgreSQL dev libraries and build tools
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy application code
COPY . .

RUN pip install -r requirements.txt && \
    mv .env.sample .env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]