import time
import sqlite3
import requests
import tweepy
import google.generativeai as genai
from bs4 import BeautifulSoup


# Twitter API Configuration
API_KEY = ''
API_SECRET = ''
ACCESS_TOKEN = '-'
ACCESS_TOKEN_SECRET = ''
BEARER_TOKEN = ''

client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Initialization of Gemini API with API Key
GOOGLE_API_KEY = ''
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def post_tweet(text, link):
    """
    Posts a tweet with the given text and link.
    """
    try:
        tweet = f"{text} {link}"
        response = client.create_tweet(text=tweet)
        print(f"Tweet published: {response.data['id']}")
    except Exception as e:
        print(f"Error posting tweet: {e}")

def create_database():
    """
    Creates a SQLite database to store news articles.
    """
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS news (title TEXT, link TEXT, content TEXT, summary TEXT)''')
    conn.commit()
    conn.close()

def delete_database():
    """
    Deletes the SQLite database.
    """
    try:
        os.remove('news.db')
    except OSError as e:
        print(f"Error deleting database: {e}")

def insert_news_into_db(news):
    """
    Inserts a list of news articles into the SQLite database.
    """
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    for article in news:
        c.execute("INSERT INTO news (title, link, content, summary) VALUES (?, ?, ?, ?)", 
                  (article['title'], article['link'], article['content'], article['summary']))
    conn.commit()
    conn.close()

def get_news_text(news_url):
    """
    Retrieves the text of a news article from the provided URL.
    """
    try:
        response = requests.get(news_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Attempt different CSS selectors based on page structure
        selectors = ['.body.vsmcontent', '.col-12.col-md-8.detail-news__main-column', '.article-main-content.article-text']
        content = None

        for selector in selectors:
            content = soup.select_one(selector)
            if content:
                break

        # Check if content was found
        if content:
            return ''.join(p.get_text(strip=True) for p in content.find_all('p'))
        else:
            return 'Content not found.'
    except requests.RequestException as e:
        return f'Error retrieving news text: {e}'

def get_lpo_news():
    """
    Retrieves news articles from 'La Politica Online'.
    """
    try:
        response = requests.get("https://www.lapoliticaonline.com")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        news = []

        for article in soup.select('.piece.ranking.standard.bordertop.breves .item.locked.nomedia')[:5]:
            title = article.find('h2', class_='title').get_text(strip=True)
            link = "https://www.lapoliticaonline.com" + article.find('a')['href']
            news_text = get_news_text(link)
            news.append({'title': title, 'link': link, 'content': news_text})

        return news

    except requests.RequestException as e:
        return f'Error making request: {e}'

def get_ambito_news():
    """
    Retrieves news articles from 'Ambito'.
    """
    try:
        response = requests.get('https://www.ambito.com')
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        news = []

        for article in soup.find('div', class_='top-ranked-news').find_all('article', class_='top-ranked-news__news-article')[:5]:
            title_tag = article.find('h2', class_='top-ranked-news__news-article-title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.find('a')['href']
                news_text = get_news_text(link)
                news.append({'title': title, 'link': link, 'content': news_text})

        return news

    except requests.RequestException as e:
        return f'Error making request: {e}'

def get_p12_news():
    """
    Retrieves news articles from 'Pagina 12'.
    """
    try:
        response = requests.get('https://www.pagina12.com.ar')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        news = []

        for article in soup.find_all('div', class_='article-title')[:5]:
            title_tag = article.find('h2', class_='article-title')
            if title_tag and title_tag.a:
                title = title_tag.get_text(strip=True)
                link = title_tag.a['href']
                news_text = get_news_text(link)
                news.append({'title': title, 'link': link, 'content': news_text})

        return news

    except requests.RequestException as e:
        return f'Error making request: {e}'

def select_random_news():
    """
    Selects a random news article from the database and deletes it.
    """
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute("SELECT * FROM news ORDER BY RANDOM() LIMIT 1")
    news_article = c.fetchone()
    if news_article:
        c.execute(
            "DELETE FROM news WHERE title = ? AND link = ?", (news_article[0], news_article[1])
            )
    conn.commit()
    conn.close()
    return news_article

def synthesize_text(text):
    """
    Synthesizes a summary of the given text using the Gemini API.
    """
    instructions = (
        "Crea un resumen en dos oraciones, ingenioso y atractivo en estilo argentino para la noticia que te presento a continuación. Incluye al menos 4 hashtags relevantes al final del resumen. "
        "El resumen debe ser conciso y llamativo, con un límite máximo de 280 caracteres y mínimo fe 160, para dejar espacio para el enlace del tweet. Noticia:"
    )
 
    text_with_instructions = instructions + text
    response = model.generate_content(text_with_instructions)
    try:
        return response.text
    except:
        pass

def process_news_articles():
    """
    Collects news articles from various sources, synthesizes summaries,
    and updates the database accordingly.
    """
    news = []
    news.extend(get_ambito_news())
    news.extend(get_p12_news())
    news.extend(get_lpo_news())

    for article in news:
        art_summary = synthesize_text(article.get('content'))
        if art_summary:
            article['summary'] = art_summary
        else:
            conn = sqlite3.connect('news.db')
            c = conn.cursor()
            c.execute("DELETE FROM news WHERE title = ?", (article['title'],))
            conn.commit()
            conn.close()

    return news_articles

def post_random_tweet():
    """
    Posts a random tweet selected from the database.
    """
    news_article = select_random_news()
    if news_article:
        text, link = news_article[3], news_article[1]
        try:
            tweet = f"{text} {link}"
            response = client.create_tweet(text=tweet)
            print(f"Tweet published: {response.data['id']}")
        except Exception as e:
            print(f"Error posting tweet: {e}")

def post_multiple_tweets(total_tweets):
    """
    Posts multiple random tweets, waiting for a specified interval between each tweet.
    :param total_tweets: The total number of tweets to post.
    """
    for i in range(total_tweets):
        post_random_tweet()
        time.sleep(73)

create_database()
news_articles = process_news_articles()
insert_news_into_db(news_articles)
post_multiple_tweets(5)
delete_database()
