from ..models import NodeTopicDataType


def topic_summary_prompt(text, existing_topics_dto):
    topic_types = [choice for choice, _ in NodeTopicDataType.choices]

    system_prompt = f"""
You are an advanced text analysis model. Your task is to analyze the provided text and produce a structured output. 
The most important part is to analyse the Topics.
Follow these instructions:

    Extract Main Topics:
        Identify the main themes or subjects discussed in the text.
        Use the provided topic IDs if relevant, but create new topics if necessary.
        Ensure that you create as few topics as possible, using proper names of people, places, or things mentioned.
        Important: Make sure to remove all topics that are not relevant to the text.
        Important: Make sure to create topic if not found in the existing topics.
        Important: Include Topics which already exist, but only if they are relevant to the text.
        Types of topics: {topic_types}
            - format dates as "dd.mm.yyyy hh:mm"

    Summarize the Content:
        Provide a concise summary of the main topic.
        Keep the summary under 200 characters.

    Format the Output in Markdown:
        Sanitize and format the text into Markdown.
        Ensure the content is equal to the original text in meaning and structure.

    Output JSON Schema:
        Use the following JSON schema for your response:

        json

    {{
      "title": "string", // a short title for the provided content
      "data_sanitized_md": "string", // the sanitized content in markdown format
      "language": "string", // the language of the content, in the form of a two-letter code (e.g., "en" for English)
      "short_summary": "string", // a short summary of the content
      "topics": [
        {{ "id": "long|null", "topic": "string", "data_type": "string" }}
      ]
    }}

Topic IDs:

    Reuse the provided topic IDs if they fit the extracted topics.
    For new topics, leave the id as null.

"""


    existing_topics_string = "\n".join([f"id: {topic['id']}, topic: {topic['topic']}, type: {topic['data_type']}" for topic in existing_topics_dto])

    user_prompt = f"""
Existing topics:
---------------
{ existing_topics_string }
    
Text: 
---------
{text}

"""
    return system_prompt, user_prompt
