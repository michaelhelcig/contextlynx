
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
- Include specific names of companies, people, cities, and other named entities as potential topics.
- Include general topics that are discussed in the text.
- If a topic already fits the content, don't create a new one, use this (with existing ID)
- If topics don't fit the content, don't include them.
- Try to introduce as few new topics as possible, BUT IMPORTANT don't miss any important ones.
- Return the Topics in Title Case

Use this JSON schema and return:
{{
'title': str, // a short title for the provided content
'data_sanitized_md': str, // the sanitized content in markdown format
'language': str, // the language of the content, in the form of a two-letter code (e.g., "en" for English)
'short_summary': str, // a short summary of the content
'topics': [
    {{ 'id': long|null, 'topic': str, 'is_new': boolean }},
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
