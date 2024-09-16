from django.templatetags.i18n import language

from ..models import NodeNote
from ..models import NodeTopic
from ..models import Edge
from .word_embedding_service import WordEmbeddingService
from .topic_service import TopicService
from .nlp_service import NlpService


class NoteService:

    def __init__(self):
        self.nlp_service = NlpService()
        self.word_embedding_service = WordEmbeddingService()
        self.topic_service = TopicService()
        pass

    def create_note(self, user, data_raw):
        existing_topics = NodeTopic.objects.filter(user=user)

        data_json = self.nlp_service.generate_topics_and_summary(data_raw, existing_topics)
        topics_json = data_json.get('topics')

        title = data_json.get('title')
        short_summary = data_json.get('short_summary')
        data_sanitized_md = data_json.get('data_sanitized_md')
        language = data_json.get('language')
        word_embedding = self.word_embedding_service.create_word_embedding(short_summary)

        note = NodeNote.objects.create(
            user=user,
            data_raw=data_raw,
            word_embedding=word_embedding,
            data_sanitized_md=data_sanitized_md,
            title=title,
            short_summary=short_summary,
            language=language,
            data_type="TEXT"
        )

        topics = set()
        topics_json = self.nlp_service.ner().get_named_entities(data_sanitized_md, topics_json)

        for topic_json in topics_json:
            topic_title = topic_json.get('title')
            topic_data_type = topic_json.get('data_type')

            topic = NodeTopic.objects.filter(user=user, title=topic_title, data_type=topic_data_type).first()

            if topic is None:
                topic = self.topic_service.create_topic(
                    user,
                    topic_title,
                    language,
                    topic_data_type
                )

            self._create_edge_for_topic(note, topic)
            topics.add(topic)

        self.topic_service.ensure_edges_for_topics(topics)

        #all_topics = NodeTopic.objects.filter(user=user)
        #self.topic_service.ensure_edges_with_similarity(all_topics, 0.85)

        return note

    def _create_edge_for_topic(self, note, topic):
        similarity = WordEmbeddingService.get_cosine_similarity(note.word_embedding.embedding_normalized, topic.word_embedding.embedding_normalized)

        edge = Edge.objects.create(
            from_node=note,
            to_node=topic,
            similarity=similarity
        )

        return edge
