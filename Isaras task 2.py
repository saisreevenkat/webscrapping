import requests
from bs4 import BeautifulSoup
import sqlite3

# Function to create the SQLite database schema
def create_schema(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            publication_date TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Function to extract articles from the Indian Express website
def extract_articles():
    url = 'https://indianexpress.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract business articles
    business_articles = []
    for article in soup.find_all('article'):
        if '/business/' in article.find('a')['href']:
            title = article.find('h2').text
            author = article.find('span', {'class': 'author'}).text
            publication_date = article.find('span', {'class': 'date'}).text
            content = article.find('div', {'class': 'content'}).text
            business_articles.append({
                'title': title,
                'author': author,
                'publication_date': publication_date,
                'content': content
            })

    return business_articles

def store_article(title, author, publication_date, content):
  """Stores the extracted article information in the database."""
  conn = sqlite3.connect('articles.db')
  cursor = conn.cursor()
  try:
    cursor.execute("""
      INSERT INTO articles (title, author, publication_date, content)
      VALUES (?, ?, ?, ?)
    """, (title, author, publication_date, content))
    conn.commit()
  except sqlite3.Error as e:
    print(f"Error storing article: {e}")
  finally:
    conn.close()


# Main function
def main():
    db_name = 'indian_express_articles.db'
    create_schema(db_name)       
    
    articles = extract_articles()
       
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    for article in articles:
        c.execute('''
                 INSERT INTO articles (title, author, publication_date, content)
                 VALUES (?, ?, ?, ?)
                 ''', (article['title'], article['author'], article['publication_date'], article['content']))
    conn.commit()
    conn.close() 


print(main)
