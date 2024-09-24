#!/bin/bash

python -m spacy download en_core_web_lg

if [ "$ENVIRONMENT" == "development" ]; then
  bash /app/scripts/entrypoint-development.sh
  exit
fi

# Wait for the database to be ready
until python manage.py migrate; do
  echo "Waiting for the database to be ready..."
  sleep 3
done

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput


# Check if NUM_WORKERS is already set
if [ -z "${NUM_WORKERS}" ]; then
  # If not set, calculate the number of workers
  NUM_WORKERS=$(nproc)
fi

# Run the application with the calculated number of workers
exec gunicorn --timeout 300 --workers $NUM_WORKERS --bind 0.0.0.0:8000 contextlynx.wsgi:application


