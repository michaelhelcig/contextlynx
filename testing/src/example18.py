import requests
from bs4 import BeautifulSoup


class WebpageScraperService:
    def __init__(self):
        pass

    def get_content(self, url):
        """
        Fetches and returns both the text content and the HTML content of the webpage at the provided URL.

        :param url: The URL of the webpage to scrape.
        :return: A tuple containing the text content and the HTML content of the webpage.
        :raises: Exception if there is an error during the HTTP request or parsing.
        """
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Get the text content
            text_content = soup.get_text(separator='\n', strip=True)

            # Get the entire HTML content
            html_content = soup.prettify()

            return text_content, html_content

        except requests.RequestException as e:
            # Handle any HTTP request errors
            print(f"An error occurred while fetching the URL: {e}")
            return None, None

        except Exception as e:
            # Handle any other errors
            print(f"An error occurred while parsing the content: {e}")
            return None, None

if __name__ == "__main__":
    scraper = WebpageScraperService()
    url = "https://example.com"  # Replace with the URL you want to scrape
    text_content, html_content = scraper.get_content(url)
    if text_content and html_content:
        print("Text Content:")
        print(text_content)
        print("\nHTML Content:")
        print(html_content)
