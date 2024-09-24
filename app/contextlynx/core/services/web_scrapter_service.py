import requests
import json
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptAvailable
from pytube import YouTube

class WebScraperService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WebScraperService, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        pass

    def get_page(self, url):
        """
        Fetches and returns both the text content and the HTML content of the webpage at the provided URL.

        :param url: The URL of the webpage to scrape.
        :return: A tuple containing the text content and the HTML content of the webpage.
        :raises: Exception if there is an error during the HTTP request or parsing.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text(separator='\n', strip=True)
            html_content = soup.prettify()

            return text_content, html_content
        except requests.RequestException as e:
            print(f"An error occurred while fetching the URL: {e}")
            return None, None
        except Exception as e:
            print(f"An error occurred while parsing the content: {e}")
            return None, None

    def get_youtube_transcript(self, video_id):
        """
        Fetches and returns the transcript of a YouTube video given its ID.

        :param video_id: The ID of the YouTube video.
        :return: The transcript of the video as a list of dictionaries containing text and timestamps.
        :raises: Exception if the transcript is not available or an API error occurs.
        """
        try:
            return YouTubeTranscriptApi.get_transcript(video_id)
        except (NoTranscriptFound, TranscriptsDisabled, NoTranscriptAvailable) as e:
            print(f"Transcript is not available for video: {video_id}. Error: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while fetching the transcript: {e}")
            return None

    def get_youtube_meta(self, video_id):
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        metadata = {
            'title': yt.title,
            'author': yt.author,
            'publish_date': yt.publish_date.strftime('%Y-%m-%d'),
            'views': yt.views,
            'length': yt.length,
            'description': yt.description,
            'thumbnail_url': yt.thumbnail_url,
            'rating': yt.rating
        }
        return metadata

    def get_youtube_transcript_sanitized(self, video_id):
        transcript = self.get_youtube_transcript(video_id)
        meta = self.get_youtube_meta(video_id)

        if transcript is not None:
            data = f"""
# YouTube Video Transcript  
Title: {meta['title']}
Author: {meta['author']}
Publish Date: {meta['publish_date']}
Description: {meta['description']}

# Transcript
"""

            for entry in transcript:
                data += entry['text'] + " "
            return data
        else:
            return None

