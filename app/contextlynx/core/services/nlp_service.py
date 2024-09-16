from ..utils import prompts
from .openai_service import OpenAiService
from .ner_service import NERService

class NlpService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NlpService, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.openai_service = OpenAiService()
        self.ner_service = NERService()

    def generate_topics_and_summary(self, text, existing_topics):
        existing_topics_dto = [{'id': topic.id, 'title': topic.title, 'data_type': topic.data_type} for topic in existing_topics]
        system_prompt, user_prompt = prompts.topic_summary_prompt(text, existing_topics_dto)
        return self.openai_service.generate_text(system_prompt, user_prompt)

    def ner(self):
        return self.ner_service
