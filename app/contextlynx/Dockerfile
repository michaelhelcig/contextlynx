# Use the official slim version of Python 3.11
FROM python:3.11-slim

# Environment variables to prevent Python from writing pyc files and to buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update and install basic build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Add Nginx configuration files for proxying
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default /etc/nginx/sites-available/default

# Setup the workdir and Python path for the non-root user
ENV PATH=~/.local/bin:$PATH
WORKDIR /app

# Install Python dependencies using pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Download python models
RUN python -m spacy download en_core_web_lg

# Copy the project code into the /app directory
COPY . .

# Make sure the user can write to some necessary files
RUN mkdir -p =staticfiles media

# Expose the port where the app will be running (Nginx)
EXPOSE 80

# Use an entrypoint script to run Gunicorn and Nginx
ENTRYPOINT ["bash", "scripts/entrypoint.sh"]