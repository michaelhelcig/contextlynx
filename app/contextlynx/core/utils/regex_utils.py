import re

def is_url(text):
    # Regular expression for validating a URL
    url_regex = re.compile(
        r'^(https?:\/\/)'  # Optional HTTP/HTTPS protocol
        r'([a-zA-Z0-9_\-]+\.)+[a-zA-Z]{2,6}'  # Domain name
        r'(\/[a-zA-Z0-9_\-@.,?^=%&:/~+#]*)?'  # Path
        r'(\?[a-zA-Z0-9_\-@.,?^=%&:/~+#]*)?'  # Query parameters
        r'(#.*)?$'  # Fragment identifier
    )
    return re.match(url_regex, text) is not None

def is_youtube_url(url):
    # Regular expression for validating a YouTube URL
    youtube_url_regex = re.compile(
        r'^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    )
    return re.match(youtube_url_regex, url) is not None

def get_youtube_id_from_url(url):
    # Regular expression to extract YouTube ID
    youtube_id_regex = re.compile(
        r'(youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    )
    match = re.search(youtube_id_regex, url)
    if match:
        return match.group(2)
    return None