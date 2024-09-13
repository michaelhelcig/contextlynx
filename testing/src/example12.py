import torch
from transformers import AutoTokenizer, AutoModel, pipeline
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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

def extract_new_topics(text, n_topics=5):
    # Get a summary of the text
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
    
    # Split the summary into potential topics
    potential_topics = summary.split(", ")
    
    # Get the embedding for the text
    text_embedding = get_embedding(text)
    
    # Get the embeddings for the potential topics and calculate their similarity to the text
    topics = []
    for topic in potential_topics:
        topic_embedding = get_embedding(topic)
        similarity = cosine_similarity([text_embedding], [topic_embedding])[0][0]
        
        # If the similarity is above a certain threshold, consider it a topic of the text
        if similarity > 0.5:
            topics.append(topic)
    
    # Limit the number of topics
    topics = topics[:n_topics]
    
    return topics

# Example usage
text = "Ruby on Rails is a comprehensive web application framework built using Ruby. It adheres to the principle of convention over configuration, simplifying development by offering predefined structures and conventions. Rails promotes rapid development and scalability, coupled with a vibrant ecosystem, making it a favored option for creating powerful and maintainable web applications."

topics = extract_new_topics(text)

print("Extracted topics:")
for topic in topics:
    print(f"- {topic}")