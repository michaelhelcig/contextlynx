FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update
RUN apt-get install build-essential -y
RUN rm -rf /var/lib/apt/lists/*

# Add a non-root user and switch to it
RUN adduser --disabled-password contextlynx
USER contextlynx

ENV PATH=~/.local/bin:$PATH

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Copy project files
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["bash", "scripts/entrypoint.sh"]
