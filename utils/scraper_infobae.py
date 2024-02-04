from utils.news_scraper import NewsScraper


class InfobaeScraper(NewsScraper):
    """
    Scraper for 'Infobae' news.
    """

    def scrape_news(self):
        """
        Method to scrape news from 'Infobae'.
        """
        soup = self._get_soup(self.base_url)
        if not soup:
            return []

        news = []
        # Find all the news items in the specified class
        for div in soup.find_all('div', class_='story-card-info')[:5]:
            title_tag = div.find('h2', class_='story-card-hl')
            link_tag = div.find('a', class_='headline-link')
            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                link = link_tag['href']
                content = self._scrape_article_content(self.base_url + link)
                if title and link and content:
                    news.append({'title': title, 'link': link, 'content': content})

        return news
