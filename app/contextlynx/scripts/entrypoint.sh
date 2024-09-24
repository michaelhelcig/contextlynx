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

# Run the application
exec gunicorn --timeout 300 --bind 0.0.0.0:8000 contextlynx.wsgi:application


