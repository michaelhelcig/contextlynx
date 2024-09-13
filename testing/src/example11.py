import torch
from transformers import AutoTokenizer, AutoModel, pipeline
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize
import numpy as np

# Download necessary NLTK data
nltk.download('punkt')

# Load pre-trained model and tokenizer for embeddings
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Load summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def extract_passage_topics(text, max_topics=5):
    # Split text into sentences
    sentences = sent_tokenize(text)
    
    # Group sentences into passages (e.g., groups of 2-3 sentences)
    passages = [' '.join(sentences[i:i+3]) for i in range(0, len(sentences), 3)]
    
    topics = []
    for passage in passages:
        # Generate a short summary for each passage
        summary = summarizer(passage, max_length=10, min_length=5, do_sample=False)[0]['summary_text']
        topics.append(summary.strip())
    
    # Remove duplicates and limit the number of topics
    topics = list(dict.fromkeys(topics))[:max_topics]
    
    return topics

def extract_topics(text, existing_topics):
    # Get embedding for the entire text
    text_embedding = get_embedding(text)
    
    # Get embeddings for existing topics
    topic_embeddings = [get_embedding(topic) for topic in existing_topics]
    
    # Calculate similarity scores for existing topics
    similarities = cosine_similarity([text_embedding], topic_embeddings)[0]
    
    # Prepare results for existing topics
    results = []
    for topic, similarity in zip(existing_topics, similarities):
        results.append({
            "topic": topic,
            "similarity": float(similarity),
            "is_new": False
        })
    
    # Extract new topics based on passage meaning
    new_topics = extract_passage_topics(text)
    
    # Calculate similarity scores for new topics and add to results
    for topic in new_topics:
        topic_embedding = get_embedding(topic)
        similarity = cosine_similarity([text_embedding], [topic_embedding])[0][0]
        results.append({
            "topic": topic,
            "similarity": float(similarity),
            "is_new": True
        })
    
    # Sort results by similarity score (descending)
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    return results

# Example usage
text = "Ruby on Rails is a comprehensive web application framework built using Ruby. It adheres to the principle of convention over configuration, simplifying development by offering predefined structures and conventions. Rails promotes rapid development and scalability, coupled with a vibrant ecosystem, making it a favored option for creating powerful and maintainable web applications."

existing_topics = [
    "Comprehensive web application framework",
    "Convention over configuration",
    "Simplifying development",
    "Predefined structures and conventions",
    "Rapid development",
    "Scalability",
    "Vibrant ecosystem",
    "Favored option",
    "Powerful and maintainable web applications"
]

results = extract_topics(text, existing_topics)

print("Topics with similarity scores:")
for result in results:
    print(f"- Topic: {result['topic']}")
    print(f"  Similarity: {result['similarity']:.4f}")
    print(f"  Is New: {result['is_new']}")
    print()