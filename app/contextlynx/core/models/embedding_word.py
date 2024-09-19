from django.db import models
from pgvector.django import VectorField
from pgvector.django import HnswIndex
from django.db import connection
from .project import Project


class WordEmbedding(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    embedding_model = models.CharField(max_length=50)
    embedding_vector = VectorField(dimensions=768)

    class Meta:
        indexes = [
            HnswIndex(
                name="word_embedding_vector",
                fields=["embedding_vector"],
                m=32,
                ef_construction=128,
                opclasses=["vector_cosine_ops"],
            )
        ]

    def __str__(self):
        return f"{self.embedding_model} - {self.id}"

    @classmethod
    def get_similar_embeddings(cls, project, embedding, threshold=0.8):
        """
        Retrieve all embeddings with cosine similarity above the given threshold using a direct database query.

        :param project: The project to filter embeddings by
        :param embedding: The embedding to compare against (WordEmbedding object or vector)
        :param threshold: The minimum cosine similarity threshold (default: 0.8)
        :return: List of tuples (id, similarity)
        """
        if isinstance(embedding, cls):
            vector = embedding.embedding_vector
        else:
            vector = embedding

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, 1 - (embedding_vector <-> %s::vector) AS similarity
                FROM core_wordembedding
                WHERE project_id = %s AND 1 - (embedding_vector <-> %s::vector) >= %s
                ORDER BY similarity DESC
            """, [vector, project.id, vector, threshold])

            results = cursor.fetchall()


        return results