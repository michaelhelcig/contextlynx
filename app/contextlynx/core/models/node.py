from django.db import models
from .user import User
from .word_embedding import WordEmbedding

class Node(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(max_length=10)
    word_embedding = models.ForeignKey(WordEmbedding, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def has_edge_to(self, node):
        raise NotImplementedError("Subclasses must implement this method.")

    def edge_to(self, node):
        raise NotImplementedError("Subclasses must implement this method.")

    def __str__(self):
        raise NotImplementedError("Subclasses must implement this method.")
