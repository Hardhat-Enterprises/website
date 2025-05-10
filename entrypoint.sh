#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

pip install django-cron

python manage.py migrate

python manage.py makemigrations

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Start the application
python manage.py runserver 0.0.0.0:8000
