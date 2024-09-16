from ..models import NodeTopicDataType


def topic_summary_prompt(text, existing_topics_dto):
    topic_types = [choice for choice, _ in NodeTopicDataType.choices]

    system_prompt = f"""
You are a Large language Model used for Topic and Context Recognition. 
You are given a text and a list the context of the text in form of topics. 


MOST IMPORTANT: REUSE TOPICS WHERE POSSIBLE 
MOST IMPORTANT: KEEP TOPICS AS GENERAL AS POSSIBLE AND AVOID SPECIFIC DETAILS 
MOST IMPORTANT: CAPTURE THE CONTEXT OF THE TEXT IN THE TOPICS

Identify the main themes or subjects discussed in the text.
Use the provided topic IDs if relevant, but create new topics if necessary.
Ensure that you create as few topics as possible, using proper names of people, places, or things mentioned.
Make sure to remove all topics that are not relevant for the text.
Make sure to create topic if not found in the existing topics.
Format the Topics in Title Case. 
    
Topic Types: {topic_types}
    
Output JSON Schema:
{{
  "title": "string", // a short title for the provided content
  "data_sanitized_md": "string", // the sanitized content in markdown format
  "language": "string", // the language of the content, in the form of a two-letter code (e.g., "en" for English)
  "short_summary": "string", // a short summary of the content under 500 chars
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
