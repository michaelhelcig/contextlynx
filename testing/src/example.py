from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

class Note:
    def __init__(self, text):
        self.id = get_next_global_id()
        self.text = text
        self.embedding = self.__get_embeddings(text)
    
    def __get_embeddings(self, text):
        """Get sentence embeddings."""
        embeddings = model.encode(text)
        return embeddings

def get_next_global_id():
    """Generate a unique ID for each note."""
    # check if the global variable exists
    if 'note_id' not in globals():
        global note_id
        note_id = 0
    note_id += 1
    return note_id

def add_note_to_graph(graph, note):
    """Add a new note to the graph and connect to similar notes based on cosine similarity."""
    new_note_id = note.id
    new_note_text = note.text
    new_note_embedding = note.embedding
    # Add new node
    graph.add_node(new_note_id, text=new_note_text, embedding=new_note_embedding)
    
    # Compute similarity with existing notes
    existing_notes = list(graph.nodes)
    existing_embeddings = [graph.nodes[n]['embedding'] for n in existing_notes]

    if existing_embeddings:
        # Compute cosine similarity
        similarities = cosine_similarity([new_note_embedding], existing_embeddings)[0]
        
        # Add edges to similar notes
        for i, existing_note_id in enumerate(existing_notes):
            if existing_note_id != new_note_id and similarities[i] > 0.1:  # Higher threshold for similarity
                graph.add_edge(new_note_id, existing_note_id, weight=similarities[i])

def main():
    # Create a sample graph
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
        "Trees are vital to our planet, offering oxygen, shade, and beauty. They support diverse ecosystems, improve air quality, and combat climate change. Protecting trees is crucial for a healthier Earth.",
        "Enzo Ferrari started his business in 1939 by founding Auto Avio Costruzioni. Initially focused on producing machine tools and aircraft accessories, the company transitioned to building race cars. In 1947, Ferrari introduced its first road car, the 125 S, marking the beginning of Ferrari as a high-performance sports car manufacturer. Enzo's deep passion for racing and his focus on engineering excellence helped establish Ferrari as an iconic brand in automotive history.",
        "Vienna, Austria's capital, is a vibrant city with over 2 million residents. Nestled on the Danube, it’s the country’s largest city and a major cultural hub. Renowned for its historic architecture, classical music, and coffeehouse culture, Vienna stands as a beacon of art and history in Central Europe."
    ]

    new_note_text = "Porsche, a German luxury car manufacturer, is renowned for its high-performance sports cars, SUVs, and sedans. Founded in 1931 by Ferdinand Porsche, the company initially focused on vehicle development and consulting. Its first car, the Porsche 356, launched in 1948, set the foundation for the brand’s future success. The iconic 911, introduced in 1964, became a symbol of engineering excellence and timeless design. Known for blending speed, precision, and luxury, Porsche remains a leader in automotive innovation. Today, the brand continues to evolve with a focus on sustainability, as seen in models like the fully electric Taycan, merging heritage with modern technology."

    # Add existing notes to the graph
    existing_notes = [Note(text) for text in existing_notes_texts]
    for note in existing_notes:
        G.add_node(note.id, text=note.text, embedding=note.embedding)
    
    # Connect similar existing notes
    for i, note1 in enumerate(existing_notes):
        for note2 in existing_notes[i + 1:]:
            similarity = cosine_similarity(
                [note1.embedding], [note2.embedding]
            )[0, 0]
            if similarity > 0.8:  # Higher similarity threshold
                G.add_edge(note1.id, note2.id, weight=similarity)
    
    # New note to be added
    new_note = Note(new_note_text)
    
    # Add new note to the graph and connect to similar notes
    add_note_to_graph(G, new_note)

    # Print the nodes and edges
    print("Nodes in the graph:")
    for node_id in G.nodes:
        print(f"ID: {node_id}, Text: {G.nodes[node_id]['text']}")
    
    print("\nEdges in the graph:")
    for edge in G.edges(data=True):
        print(f"From ID: {edge[0]}, To ID: {edge[1]}, Similarity: {edge[2]['weight']}")

if __name__ == "__main__":
    main()
