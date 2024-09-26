#!/bin/bash

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
echo "Starting Gunicorn"
exec gunicorn contextlynx.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers $NUM_WORKERS \
    --log-level=info \
    --access-logfile '-' \
    --error-logfile '-' &

# Start Nginx in the foreground
echo "Starting Nginx"
nginx -g 'daemon off;'