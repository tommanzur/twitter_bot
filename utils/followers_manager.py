import tweepy
import datetime
import time
import csv
import configparser
from utils import credentials

class FollowersManager:
    """
    A class to manage followers on Twitter, including following 
    and unfollowing accounts based on specific criteria.
    """

    def __init__(self):
        """
        Initializes the FollowersManager with a Twitter client 
        using credentials from a separate module.
        """
        self.client = tweepy.Client(
            credentials.BEARER_TOKEN,
            credentials.API_KEY,
            credentials.API_SECRET,
            credentials.ACCESS_TOKEN,
            credentials.ACCESS_TOKEN_SECRET
        )

    def authenticate_twitter_app(self, config_file):
        """
        Authenticates the Twitter application using credentials from a configuration file.

        :param config_file: Path to the configuration file containing Twitter API credentials.
        :return: An authenticated Tweepy API object.
        """
        config = configparser.ConfigParser()
        config.read(config_file)

        consumer_key = config.get("twitter", "consumer_key")
        consumer_secret = config.get("twitter", "consumer_secret")
        access_token = config.get("twitter", "access_token")
        access_secret = config.get("twitter", "access_secret")

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        return tweepy.API(auth)

    def verify_or_create_csv(self, file_name):
        """
        Verifies if a CSV file exists; if not, creates a new one with headers.

        :param file_name: Name of the CSV file to check or create.
        """
        try:
            with open(file_name, "x", newline="") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["id", "display_name", "followed_at"])
        except FileExistsError:
            pass

    def load_followed_accounts(self, file_name):
        """
        Loads a list of previously followed accounts from a CSV file.

        :param file_name: Name of the CSV file to read followed accounts from.
        :return: A list of dictionaries containing details of followed accounts.
        """
        followed = []
        with open(file_name, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip the header row
            for row in csvreader:
                followed.append({
                    "id": row[0],
                    "display_name": row[1],
                    "followed_at": datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
                })
        return followed

    def follow_accounts(
            self,
            followed,
            keywords,
            min_followers,
            max_follow_per_day,
            follow_per_hour,
            csv_file_name
            ):
        """
        Follows new accounts based on specified criteria such as keywords and minimum followers.

        :param followed: List of already followed accounts.
        :param keywords: Keywords to search in user profiles.
        :param min_followers: Minimum number of followers a user must have to be followed.
        :param max_follow_per_day: Maximum number of accounts to follow per day.
        :param follow_per_hour: Number of accounts to follow per hour.
        :param csv_file_name: CSV file name to log followed accounts.
        :return: Number of new followers.
        """
        followers_number = 0
        for follower_id in self.client.get_users_followers(followed[0].items()):
            if followers_number >= max_follow_per_day:
                break
            try:
                user = self.client.get_user(user_id=follower_id)
                if self.should_follow(user, followed, keywords, min_followers):
                    self.follow_user(user, followed, csv_file_name)
                    followers_number += 1
                    self.handle_follow_limits(followers_number, max_follow_per_day, follow_per_hour)
            except tweepy.errors.NotFound:
                print(f"User with ID {follower_id} not found.")
        return followers_number

    def should_follow(self, user, followed, keywords, min_followers):
        """
        Determines if a user should be followed based on the defined criteria.

        :param user: The user object to evaluate.
        :param followed: List of already followed accounts.
        :param keywords: Keywords to search in user profiles.
        :param min_followers: Minimum number of followers a user must have.
        :return: True if the user meets the criteria, False otherwise.
        """
        return (user.followers_count >= min_followers and
                not any(account["id"] == str(user.id) for account in followed) and
                any(keyword in user.description.lower() for keyword in keywords))

    def follow_user(self, user, followed, csv_file_name):
        """
        Follows a user and logs the action in a CSV file.

        :param user: The user object to follow.
        :param followed: List of already followed accounts to update.
        :param csv_file_name: CSV file name to log the followed account.
        """
        self.client.follow(user.id)
        followed.append({
            "id": str(user.id),
            "display_name": user.name,
            "followed_at": datetime.datetime.now()
        })
        with open(csv_file_name, "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([str(user.id), user.name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        print(f"Followed user {user.id}")

    def handle_follow_limits(self, follow, max_follow_per_day, follow_per_hour):
        """
        Manages the rate of following users to adhere to Twitter's rate limits.

        :param follow: Number of users followed in the current run.
        :param max_follow_per_day: Maximum number of accounts to follow per day.
        :param follow_per_hour: Number of accounts to follow per hour.
        """
        if follow % follow_per_hour == 0 or follow >= max_follow_per_day:
            print("Reached follow limit, sleeping for 1 hour.")
            time.sleep(3600)

    def unfollow_accounts(self, followed, unfollow_after_hours, csv_file_name):
        """
        Unfollows accounts followed more than a specified number of hours ago.

        :param followed: List of followed accounts.
        :param unfollow_after_hours: Time in hours after which to unfollow an account.
        :param csv_file_name: CSV file name to update followed accounts.
        """
        accounts_to_remove = []
        for account in followed:
            if (datetime.datetime.now() - account["followed_at"]).total_seconds() >= unfollow_after_hours * 3600:
                self.client.unfollow(account["id"])
                accounts_to_remove.append(account)
                print(f"Unfollowed user {account['id']}")

        for account in accounts_to_remove:
            followed.remove(account)

        self.update_csv_file(followed, csv_file_name)

    def update_csv_file(self, followed, csv_file_name):
        """
        Updates the CSV file with the current list of followed accounts.

        :param followed: List of currently followed accounts.
        :param csv_file_name: CSV file name to update.
        """
        with open(csv_file_name, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["id", "display_name", "followed_at"])
            for account in followed:
                csvwriter.writerow([account["id"], account["display_name"], account["followed_at"].strftime("%Y-%m-%d %H:%M:%S")])
