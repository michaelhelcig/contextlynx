from django.db import models
from pgvector.django import VectorField
from pgvector.django import HnswIndex
from django.db import connection
from .project import Project
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class WordEmbedding(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    embedding_model = models.CharField(max_length=50)
    embedding_vector = VectorField(dimensions=768)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

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
        return f"{self.embedding_model} - {self.id} (Node {self.object_id}/{self.content_type})"


    @classmethod
    def get_n_closest_neighbors(cls, project, embedding, n=10):
        """
        Retrieve the n closest embeddings using cosine similarity and a direct database query.

        :param project: The project to filter embeddings by
        :param embedding: The embedding to compare against (EmbeddingModel object or vector)
        :param n: The number of closest neighbors to retrieve (default: 10)
        :return: List of tuples (id, similarity)
        """
        return cls.get_similar_embeddings(project, embedding, threshold=0, n=n)

    @classmethod
    def get_similar_embeddings(cls, project, embedding, threshold=0.8, n=None):
        """
        Retrieve embeddings with cosine similarity above the given threshold using a direct database query.

        :param project: The project to filter embeddings by
        :param embedding: The embedding to compare against (EmbeddingModel object or vector)
        :param threshold: The minimum cosine similarity threshold (default: 0.8)
        :param max_results: The maximum number of results to return (default: None, returns all matches)
        :return: List of tuples (id, similarity)
        """
        if isinstance(embedding, cls):
            vector = embedding.embedding_vector
        else:
            vector = embedding

        table_name = cls._meta.db_table  # Get the actual table name for the model

        query = f"""
                SELECT id, 1 - (embedding_vector <-> %s::vector) AS similarity
                FROM {table_name}
                WHERE project_id = %s AND 1 - (embedding_vector <-> %s::vector) >= %s
                ORDER BY similarity DESC
            """

        params = [vector, project.id, vector, threshold]

        # check if n is not None and number
        if n is not None and isinstance(n, int):
            query += " LIMIT %s"
            params.append(n)

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()

        return results