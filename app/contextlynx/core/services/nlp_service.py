from ..utils import prompts
from .openai_service import OpenAiService
from transformers import pipeline

class NlpService:
    def __init__(self):
        self.openai_service = OpenAiService()

    def generate_topics_and_summary(self, text, existing_topics):
        existing_topics_dto = [{'id': topic.id, 'title': topic.title, 'data_type': topic.data_type} for topic in existing_topics]
        system_prompt, user_prompt = prompts.topic_summary_prompt(text, existing_topics_dto)
        return self.openai_service.generate_text(system_prompt, user_prompt)

