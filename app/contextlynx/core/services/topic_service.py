from django.contrib.contenttypes.models import ContentType
from torch.nn.functional import embedding

from .ner_service import NERService
from .word_embedding_service import WordEmbeddingService
from ..models import NodeTopic, NodeTopicType, WordEmbedding, NodeEmbedding
from ..models import Edge
from django.db import transaction

class TopicService:
    def __init__(self):
        self.word_embedding_service = WordEmbeddingService()
        self.ner_service = NERService()
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
        created = False
        topic = NodeTopic.objects.filter(project=project, title=title, data_type=data_type).first()
        if not topic:
            topics = self.search_topics_word_embedding(project, title, threshold=0.99)
            if topics:
                topic = topics[0]


        if not topic:
            topic = self.create_topic(project, title, language, data_type)
            created = True

        return topic, created


    def ensure_edges_for_topics(self, topics):
        # iterate over all topics and check if there is an edge between them
        for i, topic1 in enumerate(topics):
            topics_searched = self.search_topics_word_embedding(topic1.project, topic1.title, threshold=0.9)

            for topic2 in topics_searched:
                self.ensure_edge_for_topic_pair(topic1, topic2)

            for j, topic2 in enumerate(topics):
                if i != j:
                    self.ensure_edge_for_topic_pair(topic1, topic2)

    def search_topics_word_embedding(self, project, title, ner_split=False, threshold=0.99, limit=10):
        embedding_similarity_tupels = list()

        # split to do further NER
        if ner_split:
            # add individual named entities to the search
            named_entities = self.ner_service.get_named_entities(title)

            if named_entities:
                for named_entity in named_entities:
                    ne_title = named_entity['title']
                    embedding = self.word_embedding_service.create_word_embedding(ne_title)
                    tuples = WordEmbedding.get_n_closest_neighbors(project, embedding.embedding_vector,limit)
                    embedding_similarity_tupels.extend(tuples)


        # add entire title to the search
        embedding = self.word_embedding_service.create_word_embedding(title)
        embedding_similarity_tupels.extend(WordEmbedding.get_similar_embeddings(project, embedding.embedding_vector,
                                                                        threshold=threshold))

        # Remove empty tuples and ensure each tuple has at least two elements
        embedding_similarity_tupels = [tupel for tupel in embedding_similarity_tupels if tupel and len(tupel) > 1]
        embedding_similarity_tupels = sorted(embedding_similarity_tupels, key=lambda x: x[1], reverse=True)

        if embedding_similarity_tupels:
            topics = list()
            embeddings = [tupel[0] for tupel in embedding_similarity_tupels]
            for emb in embeddings:
                if len(topics) >= limit:
                    break
                topic = NodeTopic.for_word_embedding(emb)

                if topic:
                    topics.append(topic)
        else:
            topics = list()

        return topics

    def get_closest_neighbours(self, topic, limit=10):
        content_type = ContentType.objects.get_for_model(NodeTopic)
        embedding = topic.word_embedding.embedding_vector
        embedding_similarity_tupels = NodeEmbedding.get_n_closest_neighbors(topic.project, embedding, content_type=content_type, limit=limit)
        if embedding_similarity_tupels:
            topics = list()
            embeddings = [tupel[0] for tupel in embedding_similarity_tupels]
            for emb in embeddings:
                if len(topics) >= limit:
                    break
                topic = NodeTopic.for_word_embedding(emb)

                if topic:
                    topics.append(topic)
        else:
            topics = list()

        return topics

    def get_n_largest_topics(self, project, n):
        tupels = Edge.get_n_largest_nodes(project, ContentType.objects.get_for_model(NodeTopic), n)

        node_ids = [tupel[0] for tupel in tupels]
        return list(NodeTopic.get_by_ids(node_ids))


    @staticmethod
    def ensure_edge_for_topic_pair(topic1, topic2):
        similarity = WordEmbeddingService.get_cosine_similarity(topic1.word_embedding.embedding_vector, topic2.word_embedding.embedding_vector)
        Edge.ensure_edge(topic1, topic2, False, similarity)
