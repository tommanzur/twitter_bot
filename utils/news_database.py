import sqlite3
import os


class NewsDatabase:
    """
    A class to handle database operations for news articles storage.
    """

    def __init__(self, db_path='news.db'):
        """
        Initializes the NewsDatabase class with a specified database path.
        """
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Establishes a connection to the SQLite database."""
        self.conn = sqlite3.connect(self.db_path)

    def close(self):
        """Closes the connection to the SQLite database."""
        if self.conn:
            self.conn.close()

    def create_table(self):
        """
        Creates a table in the database to store news articles.
        The table has columns for title, link, content, and summary.
        """
        self.connect()
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS news (title TEXT, link TEXT, content TEXT, summary TEXT)''')
        self.conn.commit()
        self.close()

    def insert_news(self, article):
        """
        Inserts a list of news articles into the database.

        Args:
            news (list of dict): A list of dictionaries where each dictionary represents a news article.
        """
        self.connect()
        c = self.conn.cursor()
        c.execute("INSERT INTO news (title, link, content) VALUES (?, ?, ?)", 
                      (article['title'], article['link'], article['content']))
        self.conn.commit()
        self.close()

    def delete_database(self):
        """Deletes the SQLite database file."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def select_random_news(self):
        """
        Selects and returns a random news article from the database.

        Returns:
            tuple: A tuple containing the title, link, content, and summary of the news article.
        """
        self.connect()
        c = self.conn.cursor()
        c.execute("SELECT * FROM news ORDER BY RANDOM() LIMIT 1")
        news_article = c.fetchone()
        if news_article:
            c.execute("DELETE FROM news WHERE title = ? AND link = ?", (news_article[0], news_article[1]))
        self.conn.commit()
        self.close()
        return news_article
