from typing import List
from ..models.node import Node
import networkx as nx
from node2vec import Node2Vec
from ..models.node import Node
from ..models.edge import Edge
from sklearn.metrics.pairwise import cosine_similarity


class NodeEmbeddingService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NodeEmbeddingService, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.embedding_model = 'node2vec'
        pass

    def recalculate_node_embeddings(self, project):
        edges = Edge.objects.filter(project=project)



    def find_similar_nodes(self, nodes: List[Node], node):
        g = self._generate_graph(nodes)

        node2vec = Node2Vec(g, dimensions=96, walk_length=30, num_walks=200, workers=4)
        model = node2vec.fit(window=10, min_count=1, batch_words=4)

        embeddings = {node: model.wv[node] for node in g.nodes()}

        imilarities = cosine_similarity([new_node_embedding], list(embeddings.values()))[0]
        node_similarity_pairs = list(zip(G.nodes(), similarities))
        similar_nodes = sorted(node_similarity_pairs, key=lambda x: x[1], reverse=True)[:10]



    @staticmethod
    def _generate_graph(edges):

        g = nx.Graph()
        for edge in edges:
            g.add_edge(edge.from_node.id, edge.to_node.id)

        return g