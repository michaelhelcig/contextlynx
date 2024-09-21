from django.db import models
from pgvector.django import VectorField
from pgvector.django import HnswIndex
from .project import Project
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import connection

class NodeEmbedding(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    embedding_model = models.CharField(max_length=50)
    embedding_vector = VectorField(dimensions=96)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

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
        return f"{self.embedding_model} - {self.id} (Node {self.object_id}/{self.content_type})"


    @classmethod
    def get_n_closest_neighbors(cls, project, embedding, content_type=None, n=10):
        return cls.get_similar_embeddings(project, content_type, embedding, threshold=0, n=n)

    @classmethod
    def get_similar_embeddings(cls, project, embedding, content_type=None, threshold=0.8, n=None):
        if isinstance(embedding, cls):
            vector = embedding.embedding_vector
        else:
            vector = embedding

        table_name = cls._meta.db_table  # Get the actual table name for the model

        # Start constructing the base query
        query = f"""
                SELECT id, 1 - (embedding_vector <-> %s::vector) AS similarity
                FROM {table_name}
                WHERE project_id = %s 
                  AND 1 - (embedding_vector <-> %s::vector) >= %s
            """

        # Define the basic query params
        params = [vector, project.id, vector, threshold]

        # Add content_type filter if provided
        if content_type:
            query += " AND content_type_id = %s"
            params.append(content_type.id)

        # Add limit if n is provided
        if n is not None and isinstance(n, int):
            query += " ORDER BY similarity DESC LIMIT %s"
            params.append(n)
        else:
            # Always order by similarity if no limit
            query += " ORDER BY similarity DESC"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()

        return results

