import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class NewsScraper(ABC):
    """
    Abstract base class for scraping news from different sources.
    """

    def __init__(self, base_url):
        """
        Initialize the news scraper with a base URL.
        """
        self.base_url = base_url

    @abstractmethod
    def scrape_news(self):
        """
        Abstract method to scrape news.
        """
        pass

    def _get_soup(self, url):
        """
        Helper method to get BeautifulSoup object for a given URL.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None

    def _scrape_article_content(self, url):
        """
        Scrapes the content of a news article from the given URL.
        """
        try:
            soup = self._get_soup(url)
            if not soup:
                return 'Content not found.'

            selectors = [
                '.body.vsmcontent',
                '.col-12.col-md-8.detail-news__main-column',
                '.article-main-content.article-text',
                '[itemprop="articleBody"]',
                'div.body-article',
                '.articulo'
            ]
            content = None

            for selector in selectors:
                content = soup.select_one(selector)
                if content:
                    break

            return ''.join(
                p.get_text(strip=True) for p in content.find_all('p')
                ) if content else 'Content not found.'

        except requests.RequestException as e:
            return f'Error retrieving news text: {e}'
