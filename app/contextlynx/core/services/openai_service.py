from openai import OpenAI
from django.conf import settings
import json

class OpenAiService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OpenAiService, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"

    def get_model(self):
        return self.model

    def generate_text(self, system_prompt, user_prompt, json_format=True):
        if settings.DEBUG:
            print("System Prompt: ", system_prompt)
            print("User Prompt: ", user_prompt)

        # Create chat completion using OpenAI client with both system and user prompts
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
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
