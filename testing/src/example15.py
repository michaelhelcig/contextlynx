from transformers import BertModel, BertTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import numpy as np

# Initialize the BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_embeddings(text):
    """Get sentence embeddings using BERT."""
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    normalized_embeddings = embeddings / np.linalg.norm(embeddings)
    return normalized_embeddings

class Entity:
    def __init__(self, name):
        self.id = name
        self.embedding = get_embeddings(name)

def main():
    # Create a sample graph
    G = nx.Graph()

    # Sample names
    names = [
        "John Doe", "Jane Smith", "Alice Johnson", "Bob Brown",
        "Charlie Davis", "Alice Johnson", "Eve Williams", "Frank Miller",
        "Grace Lee", "Heidi White", "Ivan Harris", "Judy Clark",
        "Kathy Lewis", "Liam Walker", "Mia Adams", "Noah Hall"
    ]

    # Remove duplicates
    names = list(set(names))

    # Add existing notes to the graph
    entities = [Entity(name) for name in names]
    for entity in entities:
        G.add_node(entity.id, id=entity.id, embedding=entity.embedding)
    
    # Connect similar existing notes
    for i, ent1 in enumerate(entities):
        for j, ent2 in enumerate(entities):
            if ent1.id == ent2.id:
                continue

            similarity = cosine_similarity(
                [ent1.embedding], [ent2.embedding]
            )[0, 0]
            if similarity > 0.6:  # Higher similarity threshold
                G.add_edge(ent1.id, ent2.id, weight=similarity)

    # Print the nodes and edges
    print("Names in the graph:")
    for node_id in G.nodes:
        print(f"Name: {G.nodes[node_id]['id']}")
    
    print("\nEdges in the graph:")
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
    for edge in edges:
        print(f"From ID: {edge[0]}, To ID: {edge[1]}, Similarity: {edge[2]['weight']}")

if __name__ == "__main__":
    main()
