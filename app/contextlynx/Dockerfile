FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update
RUN apt-get install build-essential -y

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Download models
RUN python -m spacy download en_core_web_lg
# RUN python -c "from transformers import pipeline; pipeline('summarization', model='facebook/bart-large-cnn')"
#RUN python -c "from transformers import BertTokenizer, BertModel; BertTokenizer.from_pretrained('bert-base-uncased'); BertModel.from_pretrained('bert-base-uncased')"

# Copy project files
COPY . /app/

# Add a non-root user and switch to it
RUN adduser --disabled-password contextlynx
USER contextlynx

# Expose the port the app runs on
EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["bash", "scripts/entrypoint.sh"]
