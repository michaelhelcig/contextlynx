from .word_embedding_service import WordEmbeddingService, get_cosine_similarity
from ..models import NodeTopic
from ..models import Edge

class TopicService:
    def __init__(self):
        self.word_embedding_service = WordEmbeddingService()
        pass

    def create_topic(self, user, title, language):
        embedding = self.word_embedding_service.create_word_embedding(title)

        topic = NodeTopic.objects.create(
            user=user,
            title=title,
            language=language,
            word_embedding=embedding
        )

        return topic

    def ensure_edges_for_topics(self, topics):
        # iterate over all topics and check if there is an edge between them
        for i, topic1 in enumerate(topics):
            for j, topic2 in enumerate(topics):
                if i != j:
                    self.ensure_edge_for_topic_pair(topic1, topic2)

    def ensure_edge_for_topic_pair(self, topic1, topic2):
        if not topic1.has_edge_to(topic2) and not topic2.has_edge_to(topic1):
            similarity = get_cosine_similarity(topic1.word_embedding.embedding_normalized, topic2.word_embedding.embedding_normalized)

            Edge.objects.create(
                from_node=topic1,
                to_node=topic2,
                similarity=similarity
            )