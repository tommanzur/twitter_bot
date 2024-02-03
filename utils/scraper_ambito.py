from utils.news_scraper import NewsScraper


class AmbitoScraper(NewsScraper):
    """
    Scraper for 'Ambito' news.
    """

    def scrape_news(self):
        soup = self._get_soup(self.base_url)
        if not soup:
            return []

        news = []
        for article in soup.find('div', class_='top-ranked-news').find_all(
            'article', class_='top-ranked-news__news-article'
            )[:5]:
            title_tag = article.find('h2', class_='top-ranked-news__news-article-title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.find('a')['href']
                content = self._scrape_article_content(link)
                news.append({'title': title, 'link': link, 'content': content})
        return news
