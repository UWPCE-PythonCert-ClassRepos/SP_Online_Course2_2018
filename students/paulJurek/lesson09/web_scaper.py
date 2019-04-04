"""theading example of news downloaders

reference: https://realpython.com/intro-to-python-threading/#using-a-threadpoolexecutor"""
import threading
import concurrent.futures
import requests

WORD = "trump"

NEWS_API_KEY = "1918a54606cc493488e94ed11baf3202"

BASE_URL = 'https://newsapi.org/v1/'

# sets max number of threads which will be initiated
THREAD_LIMIT = 10

# test - test mode which limits number of records
# prod - production mode
RUN_MODE = 'test'

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
   
    url = BASE_URL + "articles"
    print(url)
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
    if RUN_MODE == 'test':
        sources = sources[:5]

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_LIMIT) as executor:
        executor.map(get_articles, sources)

