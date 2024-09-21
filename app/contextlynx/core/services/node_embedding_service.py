from django.db import transaction
import networkx as nx
from node2vec import Node2Vec
from ..models.edge import Edge
from ..models.embedding_node import NodeEmbedding
from ..models.node_topic import NodeTopic
from ..models.node_note import NodeNote


class NodeEmbeddingService:
    BASE_PATH = '/tmp/contextlynx/node_embeddings'
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NodeEmbeddingService, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.embedding_model = 'node2vec'
        self.models = {}
        pass

    def recalculate_node_embeddings(self, project):
        with transaction.atomic():
            if project.latest_node_embedding_calculated:
                return

            edges = Edge.objects.filter(project=project, predicted=False)
            model = self._get_model(project)

            note_nodes = NodeNote.objects.filter(project=project).all()
            topic_nodes = NodeTopic.objects.filter(project=project).all()
            nodes = list(note_nodes) + list(topic_nodes)
            for node in nodes:
                if str(node.id) not in model.wv.index_to_key:
                    node_embedding = [0] * 96
                else:
                    node_embedding = model.wv[str(node.id)]
                self._update_node_embedding(node, node_embedding)

            for edge in edges:
                from_node = edge.from_node
                to_node = edge.to_node

                similarity = model.wv.similarity(str(from_node.id), str(to_node.id))
                edge.similarity = similarity
                edge.save()

            # delete all predicted edges
            Edge.objects.filter(project=project, predicted=True).delete()

            project.latest_node_embedding_calculated = True
            project.save()

        #self.calculate_predicted_edges(project)

    def calculate_predicted_edges(self, project):
        with transaction.atomic():
            model = self._get_model(project)

            note_nodes = NodeNote.objects.filter(project=project).all()
            topic_nodes = NodeTopic.objects.filter(project=project).all()
            nodes = list(note_nodes) + list(topic_nodes)

            for node in nodes:
                similar_nodes = self.predict_edges(project, node, 0.8)
                for similar_node in similar_nodes:
                    similarity = model.wv.similarity(str(node.id), str(similar_node.id))
                    print(f"Predicted edge between {node.id} and {similar_node.id} with similarity {similarity}")
                    Edge.ensure_edge(node, similar_node,  True, similarity)



    def predict_edges(self, project, node, threshold=0.9):
        model = self._get_model(project)
        node_embedding = model.wv[str(node.id)]

        count = NodeTopic.count(project) + NodeNote.count(project)

        similar_nodes = model.wv.most_similar([node_embedding], topn=count)
        similar_nodes = [node for node, similarity in similar_nodes if similarity > threshold]
        similar_nodes = NodeNote.objects.filter(id__in=similar_nodes).all()

        # remove the node itself
        similar_nodes = [n for n in similar_nodes if n.id != node.id]
        return similar_nodes

    def _get_model(self, project):
        if not (project.latest_node_embedding_calculated and project.id in self.models):
            edges = Edge.objects.filter(project=project)

            g = self._generate_graph(edges)
            node2vec = Node2Vec(g, dimensions=96, walk_length=30, num_walks=200, workers=4)
            model = node2vec.fit(window=10, min_count=1, batch_words=16)
            self.models[project.id] = model

        return self.models[project.id]

    def _update_node_embedding(self, node, embedding_vector):
        try:
            if node.node_embedding is not None:
                # Delete the old embedding from the database
                embedding = node.node_embedding
                embedding.delete()
                # Set the reference to None to remove it from the object
                node.node_embedding = None
                node.save()
        except:
            pass

        # Create new embedding
        embedding = NodeEmbedding.objects.create(
            project=node.project,
            content_object=node,
            content_type=node.get_content_type(),
            embedding_model=self.embedding_model,
            embedding_vector=embedding_vector
        )

        # Assign and save the node with the updated embedding
        node.node_embedding = embedding
        node.save()

    @staticmethod
    def _generate_graph(edges):
        g = nx.Graph()
        for edge in edges:
            g.add_node(str(edge.from_node.id))
            g.add_node(str(edge.to_node.id))
            g.add_edge(str(edge.from_node.id), str(edge.to_node.id))

        return g