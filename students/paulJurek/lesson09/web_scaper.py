"""theading example of news downloaders"""
import threading

import requests

WORD = "trump"

NEWS_API_KEY = "1918a54606cc493488e94ed11baf3202"

BASE_URL = 'https://newsapi.org/v1/'

def get_sources():
    """
    get all english sources
    'https://newsapi.org/v1/sources?language=en'
    """
    url = BASE_URL + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the sources")
    print(sources)
    return sources

def get_articles(source):
    """gets articles from source"""

    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"
              }
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("something went wrong")
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    titles = [str(art['title']) + str(art['description'])
              for art in data['articles']]
    print(titles)
    return titles


if __name__ == '__main__':
    sources = get_sources()
    for i in sources:
        my_thread = threading.Thread(target=get_articles, args=(i,))
        my_thread.start()
        # my_thread.join()
