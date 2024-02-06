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

    def get_recent_tweets(self, count=10):
        """
        Gets recent tweets from the authenticated user's timeline.

        Args:
            count (int): Number of recent tweets to retrieve.

        Returns:
            List of tweet objects.
        """
        try:
            idnt=self.client.get_me().data.id
            tweets = self.client.get_users_tweets(id=idnt, max_results=count)
            return tweets.data if tweets.data else []
        except Exception as e:
            print(f"Error fetching recent tweets: {e}")
            return []

    def get_comments_and_reply(self, tweet_id):
        """
        Gets comments on a specific tweet and replies to them.

        Args:
            tweet_id (str): The ID of the tweet to get comments from.
            response_text (str): The text to reply with.
        """
        try:
            comments = []
            # Obtener menciones que podrían ser comentarios en la publicación
            mentions = self.client.get_users_mentions(id=self.client.get_me().data.id)
            for mention in mentions.data:
                if mention.referenced_tweets and mention.referenced_tweets[0].type == 'replied_to' and mention.referenced_tweets[0].id == tweet_id:
                    comments.append(mention)
                return comments
        except Exception as e:
            print(f"Error retrieving comments: {e}")
            return []

    def post_reply(self, comment_id, reply_text):
        """
        Posts a reply to a specific comment (tweet).

        Args:
            comment_id (str): The ID of the comment (tweet) to reply to.
            reply_text (str): The text of the reply.

        Returns:
            tweepy.Response: The response object from Tweepy
            if the reply is successfully posted, None otherwise.
        """
        try:
            response = self.client.create_tweet(text=reply_text, in_reply_to_tweet_id=comment_id)
            print(f"Reply posted: {response.data['id']}")
            return response
        except Exception as e:
            print(f"Error posting reply: {e}")
            return None