#!/bin/bash

# Make migrations
python manage.py makemigrations

# Wait for the database to be ready
until python manage.py migrate; do
  echo "Waiting for the database to be ready..."
  sleep 3
done

# Create superuser and set password
python manage.py shell <<EOF
from accounts.models import User

# Check if the admin user exists, if not, create it
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@admin.local', 'admin')

EOF

# Run the application
python manage.py runserver 0.0.0.0:8000
