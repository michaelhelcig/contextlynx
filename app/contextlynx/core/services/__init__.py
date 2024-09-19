from .note_service import NoteService
from .topic_service import TopicService
from .nlp_service import NlpService
from .ner_service import NERService
from .web_scrapter_service import WebScraperService
from .word_embedding_service import WordEmbeddingService
from .openai_service import OpenAiService


def init_service():
    return NlpService(), NERService(), WordEmbeddingService(), OpenAiService(), WebScraperService()
