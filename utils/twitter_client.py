import time
import tweepy
from utils.news_database import NewsDatabase


class TwitterClient:
    """
    A class to handle Twitter API interactions for posting tweets.

    Attributes:
        client (tweepy.Client): The Tweepy client for interacting with Twitter API.
        news_db (NewsDatabase): An instance of the NewsDatabase class to manage news articles.
    """

    def __init__(self, api_key, api_secret, access_token, access_token_secret, bearer_token):
        """
        Initializes the TwitterClient with Twitter API credentials.

        Args:
            api_key (str): Twitter API key.
            api_secret (str): Twitter API secret key.
            access_token (str): Twitter access token.
            access_token_secret (str): Twitter access token secret.
            bearer_token (str): Twitter bearer token.
        """
        self.client = tweepy.Client(
            bearer_token,
            api_key,
            api_secret,
            access_token,
            access_token_secret
        )
        self.news_db = NewsDatabase()

    def post_tweet_with_link(self, text, link):
        """
        Posts a tweet with the given text.

        Args:
            text (str): The text to be posted as a tweet.

        Returns:
            tweepy.Response: The response object from Tweepy
            if the tweet is successfully posted, None otherwise.
        """
        try:
            tweet = f"{text} {link}"
            response = self.client.create_tweet(text=tweet)
            print(f"Tweet published: {response.data['id']}")
        except Exception as e:
            print(f"Error posting tweet: {e}")

    def post_tweet(self, text):
        """
        Posts a tweet with the given text.

        Args:
            text (str): The text to be posted as a tweet.

        Returns:
            tweepy.Response: The response object from Tweepy
            if the tweet is successfully posted, None otherwise.
        """
        try:
            tweet = f"{text}"
            response = self.client.create_tweet(text=tweet)
            print(f"Tweet published: {response.data['id']}")
        except Exception as e:
            print(f"Error posting tweet: {e}")