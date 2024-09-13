from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import spacy
from collections import defaultdict
from sklearn.cluster import AgglomerativeClustering

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize spaCy model for Named Entity Recognition and noun phrase extraction
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError("spaCy's 'en_core_web_sm' model is not installed. Run 'python -m spacy download en_core_web_sm' to install it.")

def extract_phrases(text):
    """Extract named entities and noun phrases from text using spaCy."""
    doc = nlp(text)
    phrases = set()
    
    # Add named entities as categories
    for ent in doc.ents:
        # Include only meaningful entities
        if ent.label_ in {"PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART", "LANGUAGE"}:
            phrases.add(ent.text.lower())
    
    # Add noun chunks (phrases) as categories
    for chunk in doc.noun_chunks:
        phrases.add(chunk.text.lower())
    
    # Filter out overly specific phrases or very short ones
    filtered_phrases = {phrase.strip() for phrase in phrases if len(phrase.split()) > 1 or (len(phrase) > 4 and phrase.isalpha())}
    print(f"Extracted phrases: {filtered_phrases}")  # Debugging line
    return list(filtered_phrases)

def cluster_phrases(phrases, threshold=1.0):
    """Cluster semantically similar phrases using embeddings and cosine similarity."""
    if not phrases:
        return []

    # Get embeddings for all phrases
    embeddings = model.encode(phrases)

    # Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(embeddings)

    # Cluster phrases using Agglomerative Clustering with higher threshold
    clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=threshold, metric='precomputed', linkage='average')
    clustering.fit(1 - similarity_matrix)

    # Group phrases by their cluster label
    clustered_phrases = defaultdict(list)
    for idx, label in enumerate(clustering.labels_):
        clustered_phrases[label].append(phrases[idx])

    # Create broader categories by joining similar phrases
    broad_categories = ["; ".join(cluster) for cluster in clustered_phrases.values()]

    # Merge clusters that are semantically similar
    merged_categories = merge_similar_categories(broad_categories)
    
    print(f"Broad categories after clustering: {merged_categories}")  # Debugging line
    return merged_categories

def merge_similar_categories(categories):
    """Merge semantically similar categories into broader categories."""
    # Create high-level categories based on common themes
    theme_mapping = defaultdict(list)
    
    # Manually define themes (e.g., 'Technology', 'Nature', etc.)
    themes = {
        "Technology": ["neural networks", "swiftui", "apple", "swift", "rails", "ruby", "web application framework", "development"],
        "Nature": ["trees", "gardens", "wildlife", "air quality", "combat climate change", "our planet", "earth", "shade", "oxygen"],
        "Urban Life": ["brussels", "capital", "european union", "international politics", "cultural diversity", "architecture", "lively arts scene"],
    }
    
    # Assign categories to themes
    for category in categories:
        assigned = False
        for theme, keywords in themes.items():
            if any(keyword in category for keyword in keywords):
                theme_mapping[theme].append(category)
                assigned = True
                break
        if not assigned:  # If no matching theme, assign as is
            theme_mapping[category] = [category]
    
    # Convert theme_mapping to list of broader categories
    merged_categories = ["; ".join(phrases) for phrases in theme_mapping.values()]
    return merged_categories

class Note:
    def __init__(self, text):
        self.id = get_next_global_id()
        self.text = text
        self.embedding = self.__get_embeddings(text)
        self.phrases = extract_phrases(text)  # Extract dynamic categories from text
    
    def __get_embeddings(self, text):
        """Get sentence embeddings."""
        embeddings = model.encode(text)
        return embeddings

def get_next_global_id():
    """Generate a unique ID for each note."""
    if 'note_id' not in globals():
        global note_id
        note_id = 0
    note_id += 1
    return note_id

def add_note_to_category_graph(graph, note):
    """Add a new note to the category graph and connect categories based on similarity."""
    new_note_phrases = note.phrases
    
    # Cluster phrases to get broader categories
    broad_categories = cluster_phrases(new_note_phrases)
    
    # Add nodes for the clustered categories in the note
    for category in broad_categories:
        if not graph.has_node(category):
            graph.add_node(category)
    
    # Add edges between the categories in the new note
    for i in range(len(broad_categories)):
        for j in range(i + 1, len(broad_categories)):
            cat1 = broad_categories[i]
            cat2 = broad_categories[j]
            if not graph.has_edge(cat1, cat2):
                graph.add_edge(cat1, cat2)

def main():
    # Create a category graph
    G = nx.Graph()

    # Example existing notes
    existing_notes_texts = [
        "Cars revolutionized transportation, providing speed and convenience. They enable personal mobility, connect distant places, and have become integral to modern life. However, they also contribute to traffic congestion and pollution, highlighting the need for sustainable alternatives and innovations in automotive technology.",
        "Gardens offer a sanctuary of peace and beauty, fostering relaxation and connection with nature. They provide spaces for growing food, supporting wildlife, and improving mental well-being. A well-designed garden can transform any environment, enhancing quality of life and promoting ecological balance.",
        "Self-driving technology promises to reshape transportation by enabling vehicles to navigate and make decisions autonomously. This innovation aims to increase safety, reduce traffic congestion, and enhance efficiency. While still developing, self-driving cars have the potential to transform how we travel and interact with our environment.",
        "SwiftUI is a user interface toolkit by Apple designed for building modern, responsive applications across all Apple platforms. It simplifies UI development with a declarative syntax, allowing developers to create dynamic, adaptable interfaces. SwiftUI integrates seamlessly with Swift, enhancing productivity and streamlining code management.",
        "Ruby on Rails is a full-stack web application framework written in Ruby. It follows the convention over configuration principle, which streamlines development by providing default structures and patterns. Rails supports rapid development, scalability, and a rich ecosystem, making it a popular choice for building robust web applications.",
        "Brussels, the capital of Belgium, is a vibrant city known for its rich history and cultural diversity. It serves as the headquarters for the European Union, influencing international politics and economics. Brussels offers stunning architecture, renowned cuisine, and a lively arts scene, making it a dynamic destination.",
        "Ruby on Rails is a comprehensive web application framework built using Ruby. It adheres to the principle of convention over configuration, simplifying development by offering predefined structures and conventions. Rails promotes rapid development and scalability, coupled with a vibrant ecosystem, making it a favored option for creating powerful and maintainable web applications.",
        "Trees are vital to our planet, offering oxygen, shade, and beauty. They support diverse ecosystems, improve air quality, and combat climate change. Protecting trees is crucial for a healthier Earth."
    ]

    # Add existing notes to the graph
    existing_notes = [Note(text) for text in existing_notes_texts]
    for note in existing_notes:
        add_note_to_category_graph(G, note)
    
    # New note to be added
    new_note = Note("Neural networks and their applications")
    
    # Add new note to the graph and connect to similar notes
    add_note_to_category_graph(G, new_note)

    # Print the categories and edges
    print("Categories in the graph:")
    for node in G.nodes:
        print(f"Category: {node}")
    
    print("\nCategory Connections in the graph:")
    for edge in G.edges(data=True):
        print(f"From Category: {edge[0]}, To Category: {edge[1]}")

if __name__ == "__main__":
    main()
