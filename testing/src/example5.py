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
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    # Get model outputs
    with torch.no_grad():
        outputs = model(**inputs)
    # Get the mean of the token embeddings (last hidden state) as sentence embedding
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    # Normalize the embeddings
    normalized_embeddings = embeddings / np.linalg.norm(embeddings)
    return normalized_embeddings

class Category:
    def __init__(self, name):
        self.id = name
        self.embedding = get_embeddings(name)

def main():
    # Create a sample graph
    G = nx.Graph()

    category_names = [
        "Transportation", "Technology", "Environmental Issues",
        "Gardening", "Environmental Conservation", "Mental Health",
        "Technology", "Transportation", "Innovation",
        "Technology", "Software Development", "User Interface Design",
        "Technology", "Web Development", "Programming Languages",
        "Geography", "Culture", "European Union",
        "Technology", "Web Development", "Programming Languages",
        "Environmental Conservation", "Ecology", "Climate Change",
        "Automotive History", "Business History", "Ferrari",
        "Geography", "Culture", "History"
    ]

    # remove duplicates
    category_names = list(set(category_names))

    category_names = list()

    names2 = [
        "Tesla",
"Martin Eberhard",
"Marc Tarpenning",
"Elon Musk",
"Model S",
"Model 3",
"Model X",
"Model Y",
"Electric Vehicles",
"Renewable Energy",
"Solar Energy",
"Energy Storage Solutions",
"Powerwall",
"Automotive Industry",
"Clean Energy Solutions",
"Innovation in Technology",
"Entrepreneurship and Leadership",
    ]

    category_names.extend(names2)


    # Add existing notes to the graph
    categories = [Category(name) for name in category_names]
    for category in categories:
        G.add_node(category.id, id=category.id, embedding=category.embedding)
    
    # Connect similar existing notes
    for i, cat1 in enumerate(categories):
        for j, cat2 in enumerate(categories):
            if cat1.id == cat2.id:
                continue

            similarity = cosine_similarity(
                [cat1.embedding], [cat2.embedding]
            )[0, 0]
            if similarity > 0.6:  # Higher similarity threshold
                G.add_edge(cat1.id, cat2.id, weight=similarity)

    # Print the nodes and edges
    print("Categories in the graph:")
    for node_id in G.nodes:
        print(f"Name: {G.nodes[node_id]['id']}")
    
    print("\nEdges in the graph:")
    # order by similarity
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
    for edge in edges:
        print(f"From ID: {edge[0]}, To ID: {edge[1]}, Similarity: {edge[2]['weight']}")

if __name__ == "__main__":
    main()
