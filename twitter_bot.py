import os
import random
import time
import argparse
from utils.text_synthesizer import TextSynthesizer
from utils.twitter_client import TwitterClient
from utils.news_database import NewsDatabase
from utils.scraper_lpo import LaPoliticaOnlineScraper
from utils.scraper_ambito import AmbitoScraper
from utils.scraper_pagina12 import Pagina12Scraper
from utils.scraper_destape import ElDestapeWebScraper
from utils.scraper_infobae import InfobaeScraper
from utils.scraper_laizquierda import LaIzquierdaDiarioScraper
from utils import credentials

class NewsManager:
    """Class for manage the full process"""

    def __init__(self):
        self.twitter_client = TwitterClient(
            api_key=credentials.API_KEY,
            api_secret=credentials.API_SECRET,
            access_token=credentials.ACCESS_TOKEN,
            access_token_secret=credentials.ACCESS_TOKEN_SECRET,
            bearer_token=credentials.BEARER_TOKEN
            )
        self.news_db = NewsDatabase()
        self.text_synthesizer = TextSynthesizer(google_api_key=credentials.GOOGLE_API_KEY)
        self.scrapers = [
            LaPoliticaOnlineScraper("https://www.lapoliticaonline.com"),
            AmbitoScraper('https://www.ambito.com'),
            Pagina12Scraper('https://www.pagina12.com.ar'),
            ElDestapeWebScraper('https://www.eldestapeweb.com'),
            InfobaeScraper("https://www.infobae.com"),
            LaIzquierdaDiarioScraper('https://www.laizquierdadiario.com/')
            ]

    def process_news_articles(self):
        """Fetch and process news articles"""
        recent_articles = []
        for scraper in self.scrapers:
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

    def post_multiple_tweets(self, total_tweets, intervals=int(os.getenv('INTERVALO', 10))):
        """Post multiple tweets with intervals"""
        for _ in range(total_tweets):
            self.post_random_tweet()
            time.sleep(intervals)

    def run_publish(self, num_tweets):
        """Main method to run the news manager"""

        print("Creando base de datos...")
        self.news_db.create_table()
        print("Base de datos creada.")

        print("Procesando nuevos artículos...")
        self.process_news_articles()
        print("Nuevos artículos procesados.")

        print("Posteando nuevos tweets...")
        self.post_multiple_tweets(num_tweets)

        print("Eliminando base de datos...")
        self.news_db.delete_database()
        print("Base de datos eliminada. Proceso de publicación completado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twitter Bot para publicar noticias y más")
    parser.add_argument('--publish', action='store_true', help='Publica nuevos tweets')
    parser.add_argument('--follow_new_users', action='store_true', help='Sigue a nuevos usuarios')
    args = parser.parse_args()

    manager = NewsManager()

    if args.publish:
        num_tweets = int(os.getenv('NUM_TWEETS', 5))
        manager.run_publish(num_tweets)
    elif args.follow_new_users:
        pass