
def topic_summary_prompt(text, existing_topics_dto):
    prompt = f"""
    Analyze the following text to extract the main topics, summarize it and put it into markdown format.

    - Include specific names of companies, people, cities, and other named entities as potential topics.
    - Include the overall themes or subjects discussed in the text as topics.
    - Summarize the main topic in the text.
    - Filter out irrelevant information and focus on these named entities along with general topics.
    - If a topic already fits the content, don't create a new one, use this.
    - If topics don't fit the content, don't include them.
    - For each topic, determine if it is new (i.e., not in the list of existing topics) or if it matches one of the existing topics.
    - Return the Topics in Title Case
    - Try to keep the summary under 200 characters.
    - Try to introduce as few new topics as possible.
    - Use the ID of the existing topics if they match the content.

    Return the results as a JSON array where each entry is an object with two fields:
    - "topic": the name of the topic
    - "is_new": a boolean indicating whether the topic is new (True) or not (False)

    Use this JSON schema. NEVER CHANGE THE SCHEMA. NEVER RESPOND WITH MARKDOWN, JUST JSON:
    Return:
    {{
    'title': str, // a short title for the provided content
    'data_sanitized_md': str, // the sanitized content in markdown format
    'language': str, // the language of the content, in the form of a two-letter code (e.g., "en" for English)
    'short_summary': str, // a short summary of the content
    'topics': [
        {{ 'id': long|null, 'topic': str, 'is_new': boolean }},
    ]
    }}

    Existing topics: { existing_topics_dto }
    Text: 
    ---------
    {text}

    """

    return prompt
