from django.db import models
from .node import Node

class NodeTopic(Node):
    disabled = models.BooleanField(default=False)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title