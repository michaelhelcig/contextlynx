
def topic_summary_prompt(text, existing_topics_dto):
    existing_topics_string = "\n".join([f"id: {topic['id']}, topic: {topic['topic']}" for topic in existing_topics_dto])

    prompt = f"""
Analyze the following text to extract the main topics, summarize it and put it into markdown format.


=== Text in General ===
- Include the overall themes or subjects discussed in the text as topics.
- Summarize the main topic in the text.
- Try to keep the summary under 200 characters.
- Ensure the content is sanitized and formatted in markdown, and it is equal to the original.

=== Topics ===
- Get the most relevant context of the text in form of topics, keep them as general as possible
- IMPORTANT: Reuse the topics provided below, but only if they are relevant
- IMPORTANT: if you resuse topics, make sure to use the existing id
- IMPORTANT: Create new Topics if necessary, but try to create as few as possible.
- IMPORTANT: always create new topic, if nothing fits, but try to keep the topics as general as possible.
- Create as few topics as possible
- Create Topics from proper names of people, places, or things mentioned in the text.
- id is null for new topics, and the existing for existing topics.


Use this JSON schema and return:
{{
'title': str, // a short title for the provided content
'data_sanitized_md': str, // the sanitized content in markdown format
'language': str, // the language of the content, in the form of a two-letter code (e.g., "en" for English)
'short_summary': str, // a short summary of the content
'topics': [
    {{ 'id': long|null, 'topic': str }},
]
}}

Existing topics:
---------------
{ existing_topics_string }
    
Text: 
---------
{text}

"""
    return prompt
