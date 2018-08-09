"""
Scrape the newsAPI using threads instead of the async approach
Create a pool of threads and send a request to the pool for processing?
https://newsapi.org

EX: NewsAPI request Top business headlines in the US right now
https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=085abc22e8e24d08a97680424246aeb1
EX2: All articles about Bitcoin from the last 6 months, sorted by recent first 
https://newsapi.org/v2/everything?q=bitcoin&sortBy=publishedAt&apiKey=085abc22e8e24d08a97680424246aeb1
EX3: All articles mentioning Apple from yesterday, sorted by popular publishers first
https://newsapi.org/v2/everything?q=apple&from=2018-07-31&to=2018-07-31&sortBy=popularity&apiKey=085abc22e8e24d08a97680424246aeb1
"""

import requests
import pprint
import threading
import queue


SCRAPE_WORD = "justice"
NEWS_API_KEY = "085abc22e8e24d08a97680424246aeb1"
NEWS_API_URL = "https://newsapi.org/v2/"


def get_sources():
    """
    Get all US-based and English-language sources in NewsAPI.
    """
    url = NEWS_API_URL + "sources"
    params = {"language": "en",
              "country": "us",
              "apiKey": NEWS_API_KEY}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("All the US, English language sources:")
    for s in sources:
        print(s)
    return sources

def get_top_headlines(source):
    """
    Get top headlines from given News source
    """
    url = NEWS_API_URL + "top-headlines"
    params = {"sources": source,
              "apiKey": NEWS_API_KEY}
    print("requesting top-headlines from: " + source)
    resp = requests.get(url, params=params)
    if resp.status_code !=  200:
        print(source + " has a problem")
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    return data['articles']

def scrape_articles_queue(news_queue):
    while not news_queue.empty():
        articles = news_queue.get()
        for article in articles:
            if SCRAPE_WORD in article['title'].lower():
                print(article['source']['name'])
                print(article['title'])
                print('author: ' + str(article['author']))
                print(article['description'])
                print(article['url'])
                print()


if __name__ == '__main__':
    news_queue = queue.Queue()
    
    def add_news_queue(src):
        news_queue.put(get_top_headlines(src))

    sources = get_sources()
    threads = []
    
    for s in sources:
        thread = threading.Thread(target=add_news_queue, args=(s,))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
    
    scrape_articles_queue(news_queue)
