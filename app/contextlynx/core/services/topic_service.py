from .word_embedding_service import WordEmbeddingService
from ..models import NodeTopic, NodeTopicDataType
from ..models import Edge

class TopicService:
    def __init__(self):
        self.word_embedding_service = WordEmbeddingService()
        pass

    def create_topic(self, user, title, language, data_type=NodeTopicDataType.OTHER):
        embedding = self.word_embedding_service.create_word_embedding(title)

        topic = NodeTopic.objects.create(
            user=user,
            title=title,
            language=language,
            word_embedding=embedding,
            data_type=data_type
        )

        return topic

    def ensure_topic(self, user, title, language, data_type=NodeTopicDataType.OTHER):
        topic = NodeTopic.objects.filter(user=user, title=title, data_type=data_type).first()

        if not topic:
            topic = self.create_topic(user, title, language, data_type)

        return topic

    def ensure_edges_for_topics(self, topics):
        # iterate over all topics and check if there is an edge between them
        for i, topic1 in enumerate(topics):
            for j, topic2 in enumerate(topics):
                if i != j:
                    self.ensure_edge_for_topic_pair(topic1, topic2)

    @staticmethod
    def ensure_edges_with_similarity(nodes, similarity_threshold):
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if i != j:
                    similarity = WordEmbeddingService.get_cosine_similarity(node1.word_embedding.embedding_normalized, node2.word_embedding.embedding_normalized)
                    if similarity > similarity_threshold:
                        TopicService.ensure_edge_for_topic_pair(node1, node2)

    @staticmethod
    def ensure_edge_for_topic_pair(topic1, topic2):
        if not topic1.has_edge_to(topic2) and not topic2.has_edge_to(topic1):
            similarity = WordEmbeddingService.get_cosine_similarity(topic1.word_embedding.embedding_normalized, topic2.word_embedding.embedding_normalized)
            Edge.objects.create(
                from_node=topic1,
                to_node=topic2,
                similarity=similarity
            )
