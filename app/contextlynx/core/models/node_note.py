from django.db import models
from django.contrib.contenttypes.models import ContentType
from .node import Node
from .edge import Edge
from .node_topic import NodeTopic

class DataType(models.TextChoices):
    TEXT = 'TEXT'
    LINK = 'LINK'

class NodeNote(Node):
    title = models.CharField(max_length=255)
    short_summary = models.TextField(null=True)
    data_raw = models.TextField()
    data_type = models.CharField(max_length=10, choices=DataType.choices)
    data_sanitized_md = models.TextField()

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

    @staticmethod
    def all_edges_for_user(user):
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