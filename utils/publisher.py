import random
import time

class Publisher:
    """Class for publish new tweets"""
    def __init__(self, twitter_client, news_db, text_synthesizer):
        self.twitter_client = twitter_client
        self.news_db = news_db
        self.text_synthesizer = text_synthesizer

    def process_news_articles(self, scrapers):
        """Fetch and process news articles"""
        recent_articles = []
        for scraper in scrapers:
            recent_articles.extend(scraper.scrape_news())
            for article in recent_articles:
                self.news_db.insert_news(article)

    def post_random_tweet(self, attempt=0):
        """Post a random tweet."""
        max_attempts = 5
        if attempt > max_attempts:
            return
        news_article = self.news_db.select_random_news()
        if news_article:
            summary = self.text_synthesizer.synthesize_text(news_article[2])
            link = news_article[1]
            if len(summary) < 280:
                tweet_method = random.choice([
                    lambda: self.twitter_client.post_tweet_with_link(summary, link),
                    lambda: self.twitter_client.post_tweet(summary)
                ])
                tweet_method()
            else:
                self.post_random_tweet(attempt + 1)

    def post_multiple_tweets(self, total_tweets, intervals):
        """Post multiple tweets with intervals"""
        for _ in range(total_tweets):
            self.post_random_tweet()
            time.sleep(intervals)

    def run_publisher(self, scrapers, num_tweets, intervals):
        """Método para publicar tweets"""
        print("Procesando nuevos artículos...")
        self.process_news_articles(scrapers)
        print("Nuevos artículos procesados.")
        print("Posteando nuevos tweets...")
        self.post_multiple_tweets(num_tweets, intervals)
