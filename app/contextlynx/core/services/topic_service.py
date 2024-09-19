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
        topic = NodeTopic.objects.filter(project=project, title=title, data_type=data_type).first()
        if not topic:
            topics = self.search_topics_word_embedding(project, title, threshold=0.95)
            if topics:
                topic = topics[0]
        if not topic:
            topic = self.create_topic(project, title, language, data_type)

        return topic


    def search_topics_word_embedding(self, project, title, threshold=0.99, limit=10):
        embedding = self.word_embedding_service.create_word_embedding(title)

        embedding_similarity_tupels = WordEmbedding.get_similar_embeddings(project, embedding.embedding_vector,
                                                                        threshold=threshold)
        if embedding_similarity_tupels:
            topics = list()
            embeddings = [tupel[0] for tupel in embedding_similarity_tupels]
            for emb in embeddings:
                if len(topics) >= limit:
                    break
                topic = NodeTopic.for_word_embedding(emb)
                topics.append(topic)
        else:
            topics = list()

        return topics


    def ensure_edges_for_topics(self, topics):
        # iterate over all topics and check if there is an edge between them
        for i, topic1 in enumerate(topics):
            topics_searched = self.search_topics_word_embedding(topic1.project, topic1.title, threshold=0.85)

            for topic2 in topics_searched:
                self.ensure_edge_for_topic_pair(topic1, topic2)

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
