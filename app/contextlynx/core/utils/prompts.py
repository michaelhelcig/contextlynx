from ..models import NodeTopicDataType


def topic_summary_prompt(text, existing_topics_dto):
    topic_types = [choice for choice, _ in NodeTopicDataType.choices]

    system_prompt = f"""
You are an advanced text analysis model analyzing text and doing Named Entity Recognition!
Your task is to analyze the provided content and produce a summary of the main topics discussed using NER. 
The most important part is to analyse the Topics.
Follow these instructions:

    Extract Main Topics:
        Identify the main themes or subjects discussed in the text.
        Use the provided topic IDs if relevant, but create new topics if necessary.
        Ensure that you create as few topics as possible, using proper names of people, places, or things mentioned.
        Most Important: Always use topics provided, if they fit the content!
        Important: Make sure to remove all topics that are not relevant for the text.
        Important: Make sure to create topic if not found in the existing topics.
    
    Topic Types: {topic_types}
        
    Summarize the Content:
        Provide a concise summary of the main topic.
        Keep the summary under 500 characters.

    Format the Output in Markdown:
        Sanitize and format the text into Markdown, use headings, code, and lists where appropriate.
        Ensure the content is equal to the original text in meaning and structure.

    Output JSON Schema:
    {{
      "title": "string", // a short title for the provided content
      "data_sanitized_md": "string", // the sanitized content in markdown format
      "language": "string", // the language of the content, in the form of a two-letter code (e.g., "en" for English)
      "short_summary": "string", // a short summary of the content
      "topics": [
        {{ title: str, data_type: str }}
      ]
    }}
"""


    existing_topics_string = "\n".join([f"title: {topic['title']}, data_type: {topic['data_type']}" for topic in existing_topics_dto])

    user_prompt = f"""
Existing topics:
---------------
{ existing_topics_string }
    
Text: 
---------
{text}

"""
    return system_prompt, user_prompt
