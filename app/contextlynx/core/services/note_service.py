from .web_scrapter_service import WebScraperService
from ..models import NodeNote, Project, NodeTopic, Edge
from .word_embedding_service import WordEmbeddingService
from .node_embedding_service import NodeEmbeddingService
from .background_worker_service import BackgroundWorkerService
from .topic_service import TopicService
from .nlp_service import NlpService
from ..models.node_note import NoteDataType
from ..utils.regex_utils import is_url, is_youtube_url, get_youtube_id_from_url
from django.db import transaction


class NoteService:

    def __init__(self):
        self.nlp_service = NlpService()
        self.word_embedding_service = WordEmbeddingService()
        self.node_embedding_service = NodeEmbeddingService()
        self.background_worker_service = BackgroundWorkerService()
        self.topic_service = TopicService()
        self.web_scraper_service = WebScraperService()
        pass

    def create_note(self, user, data_input):
        with transaction.atomic():
            project = Project.get_or_create_default_project(user)
            existing_topics = NodeTopic.objects.filter(project=project)

            data_raw, data_type = self.constitute_data_raw(data_input)

            data_json = self.nlp_service.generate_topics_and_summary(data_raw, existing_topics)
            topics_json = data_json.get('topics')

            icon = data_json.get('icon')
            title = data_json.get('title')
            short_summary = data_json.get('short_summary')
            data_sanitized_md = data_json.get('data_sanitized_md')
            language = data_json.get('language')

            word_embedding = self.word_embedding_service.create_word_embedding(short_summary)
            word_embedding.project = project
            word_embedding.save()

            note = NodeNote.objects.create(
                project=project,
                data_input=data_input,
                data_raw=data_raw,
                word_embedding=word_embedding,
                data_sanitized_md=data_sanitized_md,
                icon = icon,
                title=title,
                short_summary=short_summary,
                language=language,
                data_type=data_type
            )

            project.latest_node_embedding_calculated = False
            project.save()

            topics = set()
            topics_json = self.nlp_service.ner().get_named_entities(data_sanitized_md, topics_json)

            for topic_json in topics_json:
                topic_title = topic_json.get('title')
                topic_data_type = topic_json.get('data_type')

                topic = self.topic_service.ensure_topic(project, topic_title, language, topic_data_type)

                self._create_edge_for_topic(project, note, topic)
                topics.add(topic)

            self.topic_service.ensure_edges_for_topics(topics)

            #all_topics = NodeTopic.objects.filter(project=project)
            #self.topic_service.ensure_edges_with_similarity(all_topics, 0.85)

        self.background_worker_service.recalculate_node_embeddings(project)

        return note

    def constitute_data_raw(self, data_input):
        data_input = data_input.strip()
        data_raw = data_input

        data_type = self.determine_note_data_type(data_input)

        if data_type == NoteDataType.WEBPAGE:
            if is_youtube_url(data_input):
                video_id = get_youtube_id_from_url(data_input)
                data_raw = self.web_scraper_service.get_youtube_transcript_sanitized(video_id)
                # add link to the data_raw at top as comment
                data_raw = f"# {data_input}\n{data_raw}"
            else:
                data_raw, data_raw_html = self.web_scraper_service.get_page(data_input)
                # add link to the data_raw at top as comment
                data_raw = f"# {data_input}\n{data_raw}"

        return data_raw, data_type

    @staticmethod
    def determine_note_data_type(data_input):
        data_type = NoteDataType.TEXT

        if is_url(data_input):
            data_type = NoteDataType.WEBPAGE


        return data_type

    @staticmethod
    def _create_edge_for_topic(project, note, topic):
        similarity = WordEmbeddingService.get_cosine_similarity(note.word_embedding.embedding_vector, topic.word_embedding.embedding_vector)

        edge = Edge.objects.create(
            project=project,
            from_node=note,
            to_node=topic,
            similarity=similarity
        )

        return edge

