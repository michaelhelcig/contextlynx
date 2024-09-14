import os
from openai import OpenAI
from django.conf import settings
import json
from ..utils import prompts

class GenAiService:

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"

    def _generate_text(self, prompt, json_format=True):
        if settings.DEBUG:
            print("Prompt: ", prompt)

        # Create chat completion using OpenAI client
        response = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=self.model
        )

        # Access the text from the response object properly
        response_text = response.choices[0].message.content.strip()

        if not json_format:
            return response_text

        # Parse the response assuming it is in JSON format
        try:
            # Check if wrapped in markdown
            # Trim the response text
            if response_text.startswith("```json"):
                response_text = response_text[8:-3]
            results = json.loads(response_text)
        except json.JSONDecodeError:
            print("Failed to parse JSON response:")
            print(response_text)
            results = None

        if settings.DEBUG:
            print("Response: ", response_text)
            print("Results: ", results)

        return results

    def generate_topics_and_summary(self, text, existing_topics):
        existing_topics_dto = [{'id': topic.id, 'topic': topic.title, 'is_new': False} for topic in existing_topics]
        prompt = prompts.topic_summary_prompt(text, existing_topics_dto)
        return self._generate_text(prompt)
