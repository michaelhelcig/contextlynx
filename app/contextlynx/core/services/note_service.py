from django.contrib.contenttypes.models import ContentType
from django.db.models import Case, When

from .web_scrapter_service import WebScraperService
from ..models import NodeNote, Project, NodeTopic, Edge, NodeEmbedding
from .word_embedding_service import WordEmbeddingService
from .node_embedding_service import NodeEmbeddingService
from .background_worker_service import BackgroundWorkerService
from .topic_service import TopicService
from .nlp_service import NlpService
from ..models.node_note import NoteDataType
from ..utils.regex_utils import is_url, is_youtube_url, get_youtube_id_from_url, get_urls
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

            data_raw, data_type = self._constitute_data_raw(data_input)

            existing_topics_largest = self.topic_service.get_n_largest_topics(project, 10)
            existing_topics_similar = self.topic_service.search_topics_word_embedding(project, data_raw, True, 0, 20)

            print(f"existing_topics_largest: {existing_topics_largest}")
            print(f"existing_topics_similar: {existing_topics_similar}")

            print(f"existing_topics_largest size: {len(existing_topics_largest)}")
            print(f"existing_topics_similar size: {len(existing_topics_similar)}")

            existing_topics = set(existing_topics_largest + existing_topics_similar)

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

                print(f"topic_title: {topic_title}, topic_data_type: {topic_data_type}")
                topic, created = self.topic_service.ensure_topic(project, topic_title, language, topic_data_type)
                print(f"topic: {topic}, created: {created}")

                self._create_edge_for_topic(project, note, topic)
                topics.add(topic)

            self.topic_service.ensure_edges_for_topics(topics)

        self.background_worker_service.recalculate_node_embeddings_if_necessary(project)

        return note

    def related_notes(self, note, limit: int):
        content_type = ContentType.objects.get_for_model(NodeNote)

        related_notes_tupels = Edge.get_n_nearest_nodes(note, content_type, limit)
        note_ids = [tupel[0] for tupel in related_notes_tupels]

        # Use Case and When to preserve the order of the note_ids
        preserved_order = Case(
            *[When(id=note_id, then=pos) for pos, note_id in enumerate(note_ids)]
        )

        related_notes = NodeNote.objects.filter(id__in=note_ids).order_by(preserved_order)

        return related_notes

    def _constitute_data_raw(self, data_input):
        data_input = data_input.strip()
        data_raw = data_input  # Initialize data_raw with data_input

        # Extract all URLs from the data_input
        urls = get_urls(data_input)

        print(urls)
    
        # Iterate over each URL found in data_input
        for url in urls:
            # Add URL as a comment to data_raw
            data_raw = f"# {url}\n{data_raw}"

            # Retrieve content from the URL and append it to data_raw
            if is_youtube_url(url):
                video_id = get_youtube_id_from_url(url)
                content = self.web_scraper_service.get_youtube_transcript_sanitized(video_id)
            else:
                content, _ = self.web_scraper_service.get_page(url)

            # Append the content to data_raw
            data_raw += f"\n{content}"  # Add a newline before appending content

        # Determine the data type of the original data_input
        data_type = self.determine_note_data_type(data_input)

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

        edge = Edge.ensure_edge(note, topic, False, similarity)

        return edge

