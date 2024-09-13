import torch
from transformers import AutoTokenizer, AutoModel, pipeline
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from collections import Counter

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Load pre-trained model and tokenizer for embeddings
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Load NER pipeline
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def extract_key_terms(text):
    words = word_tokenize(text)
    tagged = pos_tag(words)
    stop_words = set(stopwords.words('english'))
    key_terms = [word for word, tag in tagged if word.lower() not in stop_words and tag in ['NN', 'NNS', 'NNP', 'NNPS']]
    return [term for term in set(key_terms) if len(term) > 1]

def extract_topics(text, existing_topics, max_new_topics=10):
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
    
    # Extract new topics
    ner_results = ner_pipeline(text)
    key_terms = extract_key_terms(text)
    
    new_topics = set()
    
    # Add named entities as new topics
    for entity in ner_results:
        entity_type = entity.get('entity_group') or entity.get('entity') or ''
        entity_text = entity.get('word') or entity.get('text') or ''
        
        if entity_type in ['ORG', 'PERSON', 'PRODUCT', 'PER', 'ORG', 'MISC']:
            new_topics.add(entity_text)
    
    # Add key terms as new topics
    new_topics.update(key_terms)
    
    # Filter new topics
    new_topics = [topic for topic in new_topics if len(topic.split()) <= 2 and len(topic) >= 2]
    
    # Limit new topics
    new_topics = list(new_topics)[:max_new_topics]
    
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

# Example usagef
text = "Tesla, Inc., founded by Martin Eberhard and Marc Tarpenning in 2003, is a pioneering electric vehicle and clean energy company led by Elon Musk. The company is renowned for its innovative electric cars, such as the Model S, Model 3, Model X, and Model Y, which have significantly advanced the electric vehicle market. Tesla's advancements extend beyond cars; it also focuses on renewable energy solutions, including solar panels and energy storage products like the Powerwall. With a mission to accelerate the world's transition to sustainable energy, Tesla has become a major force in reshaping the automotive and energy industries."
existing_topics = [
    "Electric Vehicles",
    "Renewable Energy",
    "Sustainable Energy",
    "Automotive Industry",
    "Energy Storage Solutions",
    "Solar Energy",
    "Innovation in Technology",
    "Entrepreneurship and Leadership",
    "Elon Musk",
    "Clean Energy Solutions"
]

results = extract_topics(text, existing_topics)

print("Topics with similarity scores:")
for result in results:
    print(f"- Topic: {result['topic']}")
    print(f"  Similarity: {result['similarity']:.4f}")
    print(f"  Is New: {result['is_new']}")
    print()

for result in results:
    print(f"\"{result['topic']}\",")