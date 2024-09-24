from django.db import models
from django.utils.decorators import classonlymethod

from . import Project
from .embedding_node import NodeEmbedding
from .embedding_word import WordEmbedding
import uuid
from django.db import connection

class Node(models.Model):
    id = models.IntegerField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    disabled = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(max_length=10)
    node_embedding = models.ForeignKey(NodeEmbedding, on_delete=models.SET_NULL, null=True, related_name='nodes_node_embedding')
    word_embedding = models.ForeignKey(WordEmbedding, on_delete=models.SET_NULL, null=True, related_name='nodes_word_embedding')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Check if the instance is new and doesn't have an `id`
        if self.id is None:
            # Connect to the database and fetch the next value from the shared sequence
            with connection.cursor() as cursor:
                cursor.execute("SELECT nextval('node_id_seq')")
                self.id = cursor.fetchone()[0]
        # Call the real save method to actually store the object
        super().save(*args, **kwargs)

    def get_content_type(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def has_edge_to(self, node):
        raise NotImplementedError("Subclasses must implement this method.")

    def edge_to(self, node):
        raise NotImplementedError("Subclasses must implement this method.")

    def edge_count(self):
        raise NotImplementedError("Subclasses must implement this method.")

    @classonlymethod
    def count(cls, project):
        raise NotImplementedError("Subclasses must implement this method.")

    @classonlymethod
    def get_by_ids(self, node_ids):
        raise NotImplementedError("Subclasses must implement this method.")

    @classonlymethod
    def for_node_embeddings(cls, node_embedding_ids):
        raise NotImplementedError("Subclasses must implement this method.")

    @classonlymethod
    def for_word_embedding(cls, word_embedding_id):
        raise NotImplementedError("Subclasses must implement this method.")

    @classonlymethod
    def for_node_embedding(cls, word_embedding_id):
        raise NotImplementedError("Subclasses must implement this method.")

    @staticmethod
    def all_edges_for_project(user):
        raise NotImplementedError("Subclasses must implement this method.")

    def __str__(self):
        raise NotImplementedError("Subclasses must implement this method.")
