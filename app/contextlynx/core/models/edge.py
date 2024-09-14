from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Edge(models.Model):
    from_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='from_edges')
    from_object_id = models.PositiveIntegerField()
    from_node = GenericForeignKey('from_content_type', 'from_object_id')

    to_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='to_edges')
    to_object_id = models.PositiveIntegerField()
    to_node = GenericForeignKey('to_content_type', 'to_object_id')

    similarity = models.FloatField()

    def __str__(self):
        return f"{self.from_node} -> {self.to_node} ({self.similarity})"
