import os
import argparse
from utils.publisher import Publisher
from utils.followers_manager import FollowersManager
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

MIN_FOLLOWERS = 100
KEYWORDS = ["argentina"]
MAX_FOLLOW_PER_DAY = 200
FOLLOW_PER_HOUR = 15
UNFOLLOW_AFTER_HOURS = 36
CSV_FILE_NAME = "followed_accounts.csv"

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
        self.publisher = Publisher(
            self.twitter_client,
            self.news_db,
            self.text_synthesizer
        )

    def run_publish(self, n_tweets):
        """Método para publicar tweets"""
        print("Creando base de datos...")
        self.news_db.create_table()
        print("Base de datos creada.")
        self.publisher.run_publisher(self.scrapers, n_tweets, int(os.getenv('INTERVALO', 10)))
        print("Eliminando base de datos...")
        self.news_db.delete_database()
        print("Base de datos eliminada. Proceso de publicación completado.")

    def run_reply(self):
        """Método para responder a comentarios en publicaciones recientes."""
        recent_tweets = self.twitter_client.get_recent_tweets(count=15)
        for tweet in recent_tweets:
            comments = self.twitter_client.get_comments_and_reply(tweet['id'])
            for comment in comments:
                synthesized_reply = self.text_synthesizer.synthesize_reply(comment['text'])
                if synthesized_reply:
                    self.twitter_client.post_reply(comment['id'], synthesized_reply)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twitter Bot para publicar noticias y más")
    parser.add_argument('--publish', action='store_true', help='Publica nuevos tweets')
    parser.add_argument('--manage_followers', action='store_true', help='Administrar seguidores en Twitter')
    parser.add_argument('--reply', action='store_true', help='Publica respuestas a los comentarios en los tweets')
    args = parser.parse_args()

    manager = NewsManager()

    if args.publish:
        num_tweets = int(os.getenv('NUM_TWEETS', 5))
        manager.run_publish(num_tweets)
    if args.manage_followers:
        follower_manager = FollowersManager()
        follower_manager.verify_or_create_csv(CSV_FILE_NAME)
        followed_accounts = follower_manager.load_followed_accounts(CSV_FILE_NAME)
        follower_manager.follow_accounts(
            followed_accounts,
            KEYWORDS,
            MIN_FOLLOWERS,
            MAX_FOLLOW_PER_DAY,
            FOLLOW_PER_HOUR,
            CSV_FILE_NAME
        )
        follower_manager.unfollow_accounts(followed_accounts, UNFOLLOW_AFTER_HOURS, CSV_FILE_NAME)
    if args.reply:
        print("Respondiendo a comentarios...")
        manager.run_reply()
        print("Respuestas completadas.")
