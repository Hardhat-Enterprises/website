#!/bin/bash

echo "Starting Django server with automatic image optimization..."
echo

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found. Please run this from the website directory."
    exit 1
fi

# Run the server with optimization
python manage.py runserver_with_optimization
