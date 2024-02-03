from utils.news_scraper import NewsScraper


class ElDestapeWebScraper(NewsScraper):
    """
    Scraper for 'El Destape' news.
    """

    def scrape_news(self):
        """
        Method to scrape news from 'El Destape Web'.
        """
        soup = self._get_soup(self.base_url)
        if not soup:
            return []

        news = []
        for div in soup.find_all('div', class_='titulo')[:5]:
            title_tag = div.find('h2')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = self.base_url + title_tag.find('a')['href']
                content = self._scrape_article_content(link)
                news.append({'title': title, 'link': link, 'content': content})

        return news
