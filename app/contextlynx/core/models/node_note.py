from django.db import models
from .node import Node

class DataType(models.TextChoices):
    TEXT = 'TEXT'
    LINK = 'LINK'

class NodeNote(Node):
    title = models.CharField(max_length=255)
    short_summary = models.CharField(max_length=255, null=True)
    data_raw = models.TextField()
    data_type = models.CharField(max_length=4, choices=DataType.choices)
    data_sanitized_md = models.TextField()

    def __str__(self):
        return self.title