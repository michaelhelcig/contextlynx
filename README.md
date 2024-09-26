# ContextLynx

**ContextLynx** is a next-generation **Personal Knowledge Management (PKM)** tool designed to eliminate the need for manual categorization or tagging of notes. By leveraging advanced natural language processing techniques, ContextLynx organizes and connects your notes seamlessly through a dynamic knowledge graph. The application automatically detects relationships between your ideas, notes, and research topics, making your knowledge organization smarter and more intuitive. You can try out the service at [contextlynx.com/get-started](http://contextlynx.com/get-started).

## Features

- **Semantic Note Taking**: Automatically detects connections between your notes using local models for Named Entity Recognition (NER) and word embeddings, alongside powerful large language models (LLMs) accessed via APIs.
  
- **Knowledge Graph**: Visualize your notes and their relationships in a knowledge graph, helping you explore topics holistically.

- **Supported Inputs**:
  - **Plain Text**: Write or import plain text notes.
  - **Web Links**: Automatically scrape and extract content from websites to capture information.
  - **YouTube Links**: Extract transcripts from YouTube videos to integrate their content into your knowledge graph.

- **Machine Learning Predictions**: Using node and graph embeddings (via **Node2Vec**), the app predicts which notes are likely to be connected based on the content.

- **LLM-Driven Context**: Leverage large language models to get deeper insights into the context of your notes, enhancing understanding and discovery of new connections.

## Technical Details

- **Backend**: Written entirely in Python, ContextLynx combines local machine learning models with API-based access to large LLMs for context generation. The application is built on the Django framework.

- **Graph Embeddings**: Utilizes Node2Vec for generating node/graph embeddings, enabling ML-driven predictions about note relationships.

- **Course Project**: This project was developed as part of the "Knowledge Graph" course at **TU Wien**.

## Deployment

You can try out ContextLynx live at [contextlynx.com/get-started](http://contextlynx.com/get-started).

### Dependencies
* Docker

### Local Deployment

To deploy ContextLynx locally, you'll need **Docker** installed on your machine. Follow these steps:

1. Clone the repository.
2. Copy the environment template file `.env.template` to `.env`:
   ```bash
   cp .env.template .env
   ```
3. The OpenAI API key is not included in the repository. You'll need to create your own API key by signing up and generating one at:
https://platform.openai.com/organization/api-keys
4. Start the service using Docker Compose:
   ```bash
   docker-compose up --build
   ```
5. Visit http://localhost:8000/get-started