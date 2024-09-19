from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptAvailable
import re
import json

def get_youtube_transcript(video_id):
    """
    Fetches and returns the transcript of a YouTube video given its ID.

    :param video_id: The ID of the YouTube video.
    :return: The transcript of the video as a list of dictionaries containing text and timestamps.
    :raises: Exception if the transcript is not available or an API error occurs.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except (NoTranscriptFound, TranscriptsDisabled, NoTranscriptAvailable) as e:
        print(f"Transcript is not available for video: {video_id}. Error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while fetching the transcript: {e}")
        return None


def get_youtube_id_from_url(url):
    # Regular expression to extract YouTube ID
    youtube_id_regex = re.compile(
        r'(youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    )
    match = re.search(youtube_id_regex, url)
    if match:
        return match.group(2)
    return None



url = "https://www.youtube.com/watch?v=ZIyB9e_7a4c"

video_id = get_youtube_id_from_url(url)
transcript = get_youtube_transcript(video_id)

# format json output
transcript = json.dumps(transcript, indent=4)
print(transcript)

