from django.db import models
from django.contrib.contenttypes.models import ContentType
from .node import Node
from .edge import Edge
from .node_topic import NodeTopic
from .embedding_node import NodeEmbedding
from .embedding_word import WordEmbedding

class NoteDataType(models.TextChoices):
    TEXT = 'TEXT'
    WEBPAGE = 'WEBPAGE'

class NodeNote(Node):
    icon = models.CharField(max_length=16, default='🗒')
    title = models.CharField(max_length=255)
    short_summary = models.TextField(null=True)
    data_input = models.TextField()
    data_raw = models.TextField()
    data_type = models.CharField(max_length=10, choices=NoteDataType.choices)
    data_sanitized_md = models.TextField()

    node_embedding = models.ForeignKey(
        NodeEmbedding, on_delete=models.SET_NULL, null=True,
        related_name='note_node_embeddings'
    )
    word_embedding = models.ForeignKey(
        WordEmbedding, on_delete=models.SET_NULL, null=True,
        related_name='note_word_embeddings'
    )

    def has_edge_to(self, node):
        """
        Check if there is an edge from this NodeTopic to the given node.
        """
        # Ensure the node's content type is the same as NodeTopic
        from_content_type = ContentType.objects.get_for_model(self)
        to_content_type = ContentType.objects.get_for_model(node)

        return Edge.objects.filter(
            from_content_type=from_content_type,
            from_object_id=self.id,
            to_content_type=to_content_type,
            to_object_id=node.id
        ).exists()

    def edge_to(self, node):
        """
        Get the edge from this NodeTopic to the given node.
        """
        # Ensure the node's content type is the same as NodeTopic
        from_content_type = ContentType.objects.get_for_model(self)
        to_content_type = ContentType.objects.get_for_model(node)

        return Edge.objects.get(
            from_content_type=from_content_type,
            from_object_id=self.id,
            to_content_type=to_content_type,
            to_object_id=node.id
        )

    def edge_count(self):
        return Edge.objects.filter(
            from_content_type=ContentType.objects.get_for_model(self),
            from_object_id=self.id
        ).count()


    def related_topics(self, depth = 1):
        """
        Get all related topics for this note.
        """
        # Get all edges from this note
        edges = Edge.objects.filter(
            from_content_type=ContentType.objects.get_for_model(self),
            from_object_id=self.id,
            to_content_type=ContentType.objects.get_for_model(NodeTopic)
        )

        # Get all topics from these edges
        topics = [edge.to_node for edge in edges]

        return topics

    @classmethod
    def for_word_embedding(cls, word_embedding_id):
        return cls.objects.get(word_embedding_id=word_embedding_id)

    @classmethod
    def for_node_embedding(cls, node_embedding_id):
        return cls.objects.get(node_embedding_id=node_embedding_id)

    @staticmethod
    def all_edges_for_project(user):
        # Get all Node instances for the user
        node_ct = ContentType.objects.get_for_model(NodeNote)
        nodes = NodeNote.objects.filter(user=user)

        node_ids = nodes.values_list('id', flat=True)

        return Edge.objects.filter(
            from_content_type=node_ct,
            from_object_id__in=node_ids
        )

    def __str__(self):
        return self.title