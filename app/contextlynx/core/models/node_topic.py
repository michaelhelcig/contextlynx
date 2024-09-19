from django.db import models
from .node import Node
from .edge import Edge
from django.contrib.contenttypes.models import ContentType
from .embedding_node import NodeEmbedding
from .embedding_word import WordEmbedding

class NodeTopicType(models.TextChoices):
    OTHER = 'OTHER'
    CONCEPT = 'CONCEPT'
    PERSON = 'PERSON'
    ORGANIZATION = 'ORGANIZATION'
    LOCATION = 'LOCATION'
    DATE = 'DATE'
    EVENT = 'EVENT'
    PRODUCT = 'PRODUCT'
    WORK_OF_ART = 'WORK_OF_ART'
    LAW = 'LAW'
    LANGUAGE = 'LANGUAGE'
    QUANTITY = 'QUANTITY'
    PERCENT = 'PERCENT'
    MONEY = 'MONEY'
    TIME = 'TIME'
    URL = 'URL'
    EMAIL = 'EMAIL'
    PHONE_NUMBER = 'PHONE_NUMBER'
    NATIONALITY = 'NATIONALITY'
    RELIGION = 'RELIGION'
    TITLE = 'TITLE'
    VEHICLE = 'VEHICLE'
    ANIMAL = 'ANIMAL'
    PLANT = 'PLANT'
    MEDICAL_CONDITION = 'MEDICAL_CONDITION'
    SPORTS_TEAM = 'SPORTS_TEAM'
    INDUSTRY = 'INDUSTRY'
    COMPANY = 'COMPANY'


class NodeTopic(Node):
    disabled = models.BooleanField(default=False)
    title = models.CharField(max_length=512)
    data_type = models.CharField(max_length=20, choices=NodeTopicType.choices, default=NodeTopicType.OTHER)
    language = models.CharField(max_length=10)

    node_embedding = models.ForeignKey(
        NodeEmbedding, on_delete=models.SET_NULL, null=True,
        related_name='topic_node_embeddings'
    )
    word_embedding = models.ForeignKey(
        WordEmbedding, on_delete=models.SET_NULL, null=True,
        related_name='topic_word_embeddings'
    )

    def has_edge_to(self, node):
        """
        Check if there is an edge from this NodeTopic to the given node.
        """
        # Ensure the node's content type is the same as NodeTopic
        from_content_type = ContentType.objects.get_for_model(self)
        to_content_type = ContentType.objects.get_for_model(node)

        return Edge.objects.filter(
            from_content_type=from_content_type,
            from_object_id=self.id,
            to_content_type=to_content_type,
            to_object_id=node.id
        ).exists()

    def edge_to(self, node):
        """
        Get the edge from this NodeTopic to the given node.
        """
        # Ensure the node's content type is the same as NodeTopic
        from_content_type = ContentType.objects.get_for_model(self)
        to_content_type = ContentType.objects.get_for_model(node)

        return Edge.objects.get(
            from_content_type=from_content_type,
            from_object_id=self.id,
            to_content_type=to_content_type,
            to_object_id=node.id
        )

    def edge_count(self):
        return Edge.objects.filter(
            from_content_type=ContentType.objects.get_for_model(self),
            from_object_id=self.id
        ).count()

    @classmethod
    def for_word_embedding(cls, word_embedding_id):
        return cls.objects.get(word_embedding_id=word_embedding_id)

    @classmethod
    def for_node_embedding(cls, node_embedding_id):
        return cls.objects.get(node_embedding_id=node_embedding_id)

    def __str__(self):
        return self.title
