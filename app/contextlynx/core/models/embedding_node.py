from django.db import models
from pgvector.django import VectorField
from pgvector.django import HnswIndex
from .project import Project

class NodeEmbedding(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    embedding_model = models.CharField(max_length=50)
    embedding_vector = VectorField(dimensions=96)

    class Meta:
        indexes = [
            HnswIndex(
                name="node_embedding_vector",
                fields=["embedding_vector"],
                m=32,
                ef_construction=128,
                opclasses=["vector_cosine_ops"],
            )
        ]

    def __str__(self):
        return f"{self.embedding_model} - {self.id}"