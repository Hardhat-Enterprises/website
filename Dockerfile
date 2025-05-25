FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK and TextBlob corpora
RUN python -m textblob.download_corpora
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab', raise_on_error=False); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/static /app/media

# Run migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi"]