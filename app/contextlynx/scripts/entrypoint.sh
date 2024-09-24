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

# Determine the number of CPU cores
NUM_CORES=$(nproc)

# Calculate the number of workers
NUM_WORKERS=$((2 * NUM_CORES + 1))

# Run the application with the calculated number of workers
exec gunicorn --timeout 300 --workers $NUM_WORKERS --bind 0.0.0.0:8000 contextlynx.wsgi:application


