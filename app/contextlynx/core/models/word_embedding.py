from django.db import models
from django.contrib.postgres.fields import ArrayField

class WordEmbedding(models.Model):
    model = models.CharField(max_length=50)
    embedding_normalized = models.JSONField()

    def __str__(self):
        return f"{self.model} - {self.id}"

