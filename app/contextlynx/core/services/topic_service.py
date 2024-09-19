from torch.nn.functional import embedding

from .word_embedding_service import WordEmbeddingService
from ..models import NodeTopic, NodeTopicType, WordEmbedding
from ..models import Edge
from django.db import transaction

class TopicService:
    def __init__(self):
        self.word_embedding_service = WordEmbeddingService()
        pass

    def create_topic(self, project, title, language, data_type=NodeTopicType.OTHER):
        with transaction.atomic():
            embedding = self.word_embedding_service.create_word_embedding(title)
            embedding.project = project
            embedding.save()

            topic = NodeTopic.objects.create(
                project=project,
                title=title,
                language=language,
                word_embedding=embedding,
                data_type=data_type
            )

            return topic

    def ensure_topic(self, project, title, language, data_type=NodeTopicType.OTHER):
        topic = self.search_topic(project, title, language, data_type)

        if not topic:
            topic = self.create_topic(project, title, language, data_type)

        return topic


    def search_topic(self, project, title, language, data_type=NodeTopicType.OTHER):
        topic = NodeTopic.objects.filter(project=project, title=title, data_type=data_type).first()

        if not topic:
            embedding = self.word_embedding_service.create_word_embedding(title)

            embedding_similarity_map = WordEmbedding.get_similar_embeddings(project, embedding.embedding_vector,
                                                                            threshold=0.99)
            if embedding_similarity_map:
                embedding_similarity = embedding_similarity_map[0]
                topic = NodeTopic.for_word_embedding(embedding_similarity[0])
            else:
                topic = None

        return topic

    def ensure_edges_for_topics(self, topics):
        # iterate over all topics and check if there is an edge between them
        for i, topic1 in enumerate(topics):
            for j, topic2 in enumerate(topics):
                if i != j:
                    self.ensure_edge_for_topic_pair(topic1, topic2)

    @staticmethod
    def ensure_edge_for_topic_pair(topic1, topic2):
        if not topic1.has_edge_to(topic2) and not topic2.has_edge_to(topic1):
            similarity = WordEmbeddingService.get_cosine_similarity(topic1.word_embedding.embedding_vector, topic2.word_embedding.embedding_vector)
            Edge.objects.create(
                project=topic1.project,
                from_node=topic1,
                to_node=topic2,
                similarity=similarity
            )
