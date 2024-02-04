from utils.news_scraper import NewsScraper

class LaIzquierdaDiarioScraper(NewsScraper):
    """
    Scraper for 'La Izquierda Diario' news.
    """

    def scrape_news(self):
        """
        Method to scrape news from 'La Izquierda Diario'.
        """
        soup = self._get_soup(self.base_url)
        if not soup:
            return []

        news = []
        for div in soup.find_all('div', class_='noticia noticia4lineas')[:5]:
            title_tag = div.find('h3')
            link_tag = title_tag.find('a') if title_tag else None
            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                link = link_tag['href']
                content = self._scrape_article_content(self.base_url + link)
                if title and link and content:
                    news.append({'title': title, 'link': link, 'content': content})

        return news
