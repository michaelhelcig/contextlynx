from django.db import models
from django.utils.decorators import classonlymethod

from . import Project
from .embedding_node import NodeEmbedding
from .embedding_word import WordEmbedding
import uuid

class Node(models.Model):
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
