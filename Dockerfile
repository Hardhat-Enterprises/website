FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies including development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    vim \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install additional development dependencies
RUN pip install --no-cache-dir \
    ipython \
    ipdb \
    django-debug-toolbar \
    django-extensions

# Create necessary directories first
RUN mkdir -p /app/static /app/media

# Database population is handled by Django management command in docker-compose

# Copy project (this will be overridden by volume mount in development)
COPY . .

# Ensure .env file exists for SECRET_KEY persistence
RUN touch /app/.env

# Development command - will be overridden by docker-compose
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--insecure"] 