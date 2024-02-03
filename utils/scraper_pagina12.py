from utils.news_scraper import NewsScraper


class Pagina12Scraper(NewsScraper):
    """
    Scraper for 'Pagina 12' news.
    """

    def scrape_news(self):
        """
        Method to scrape news.
        """
        soup = self._get_soup(self.base_url)
        if not soup:
            return []

        news = []
        for article in soup.find_all('div', class_='article-title')[:5]:
            title_tag = article.find('h2', class_='article-title')
            if title_tag and title_tag.a:
                title = title_tag.get_text(strip=True)
                link = title_tag.a['href']
                content = self._scrape_article_content(link)
                news.append({'title': title, 'link': link, 'content': content})
        return news
