from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from .project import Project
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .node import Node
import uuid

class Edge(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    from_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='from_edges')
    from_object_id = models.PositiveIntegerField()
    from_node = GenericForeignKey('from_content_type', 'from_object_id')

    to_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='to_edges')
    to_object_id = models.PositiveIntegerField()
    to_node = GenericForeignKey('to_content_type', 'to_object_id')

    similarity = models.FloatField()

    @staticmethod
    def get_for_nodes(nodes):
        node_ct = ContentType.objects.get_for_model(Node)

        node_ids = nodes.values_list('id', flat=True)
        node_ct_ids = [node_ct.id] * len(node_ids)  # Same content type for all nodes

        # Filter edges where the 'from_node' matches these node IDs
        froms = Edge.objects.filter(
            from_content_type=node_ct,
            from_object_id__in=node_ids
        )

        tos = Edge.objects.filter(
            to_content_type=node_ct,
            to_object_id__in=node_ids
        )

        return froms.union(tos)

    def __str__(self):
        return f"{self.from_node} -> {self.to_node} ({self.similarity})"
