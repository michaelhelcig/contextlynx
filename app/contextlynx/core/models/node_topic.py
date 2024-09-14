from django.db import models
from .node import Node
from .edge import Edge
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

class NodeTopic(Node):
    disabled = models.BooleanField(default=False)
    title = models.CharField(max_length=255)

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

    def __str__(self):
        return self.title
