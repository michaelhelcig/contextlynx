from ..models import NodeNote
from ..models import NodeTopic
from ..models import Edge
from .word_embedding_service import WordEmbeddingService, get_cosine_similarity
from .topic_service import TopicService
from .genai_service import GenAiService

class NoteService:

    def __init__(self):
        self.gen_ai_service = GenAiService()
        self.word_embedding_service = WordEmbeddingService()
        self.topic_service = TopicService()
        pass

    def create_note(self, user, data_raw):
        existing_topics = NodeTopic.objects.filter(user=user)

        sanitized_json = self.gen_ai_service.generate_topics_and_summary(data_raw, existing_topics)
        topics_json = sanitized_json.get('topics')

        short_summary = sanitized_json.get('short_summary')
        word_embedding = self.word_embedding_service.create_word_embedding(short_summary)

        note = NodeNote.objects.create(
            user=user,
            data_raw=data_raw,
            word_embedding=word_embedding,
            data_sanitized_md=sanitized_json.get('data_sanitized_md'),
            title=sanitized_json.get('title'),
            short_summary=sanitized_json.get('short_summary'),
            language=sanitized_json.get('language'),
            data_type="TEXT"
        )

        topics = set()
        for topic_json in topics_json:
            if topic_json.get('is_new') == True:
                topic = self.topic_service.create_topic(
                    user,
                    topic_json.get('topic'),
                    sanitized_json.get('language'))
            elif topic_json.get('id') != None:
                topic = NodeTopic.objects.get(id=topic_json.get('id'))

            self._create_edge_for_topic(note, topic)
            topics.add(topic)

        self.topic_service.ensure_edges_for_topics(topics)
        return note

    def _create_edge_for_topic(self, note, topic):
        similarity = get_cosine_similarity(note.word_embedding.embedding_normalized, topic.word_embedding.embedding_normalized)

        edge = Edge.objects.create(
            from_node=note,
            to_node=topic,
            similarity=similarity
        )

        return edge
