from utils.news_scraper import NewsScraper


class LaPoliticaOnlineScraper(NewsScraper):
    """
    Scraper for 'La Politica Online' news.
    """

    def scrape_news(self):
        soup = self._get_soup(self.base_url)
        if not soup:
            return []
        news = []
        for article in soup.select(
            '.piece.ranking.standard.bordertop.breves .item.locked.nomedia'
            )[:4]:
            title = article.find('h2', class_='title').get_text(strip=True)
            link = self.base_url + article.find('a')['href']
            content = self._scrape_article_content(link)
            news.append({'title': title, 'link': link, 'content': content})
        return news
