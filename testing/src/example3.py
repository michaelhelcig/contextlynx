from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import networkx as nx

def extract_topics_lda(texts, num_topics=5):
    """Extract topics from texts using LDA."""
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    lda.fit(X)
    
    feature_names = vectorizer.get_feature_names_out()
    
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[-10:]  # Get the top words for each topic
        top_words = [feature_names[i] for i in top_words_idx]
        topics.append(" ".join(top_words))
    
    return topics

def add_note_to_category_graph(graph, note):
    """Add a new note to the category graph and connect categories based on similarity."""
    # Extract topics from the new note
    topics = extract_topics_lda([note.text])
    
    # Add nodes for the topics
    for topic in topics:
        if topic and not graph.has_node(topic):
            graph.add_node(topic)
    
    # Add edges between topics (if needed)
    for i in range(len(topics)):
        for j in range(i + 1, len(topics)):
            topic1 = topics[i]
            topic2 = topics[j]
            if topic1 and topic2 and not graph.has_edge(topic1, topic2):
                graph.add_edge(topic1, topic2)

class Note:
    def __init__(self, text):
        self.id = get_next_global_id()
        self.text = text
    
def get_next_global_id():
    """Generate a unique ID for each note."""
    if 'note_id' not in globals():
        global note_id
        note_id = 0
    note_id += 1
    return note_id

def main():
    # Create a category graph
    G = nx.Graph()

    # Example notes
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
    
    # Add new note to the graph and connect to categories
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
