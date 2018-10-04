# -*- coding: utf-8 -*-
"""
A version of the news-gathering script that uses threading instead of asynch
"""

import threading
import time
import requests
from queue import Queue

WORD = "trump"

NEWS_API_KEY = "5d237a99c69842c58b9a90b28d9d9581"

base_url = 'https://newsapi.org/v1/'

q = Queue() # No thread limits, search takes 4.14 seconds
q = Queue(maxsize = 10) # Search takes 3.65 seconds
q = Queue(maxsize = 20)

def get_sources():
    """
    Get all the english language sources of news

    'https://newsapi.org/v1/sources?language=en'
    """
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the sources")
    print(sources)
    return sources

def get_articles(source):
    """
    https://newsapi.org/v1/articles?source=associated-press&sortBy=top&apiKey=1fabc23bb9bc485ca59b3966cbd6ea26
    """
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              # "sortBy": "latest", # some sources don't support latest
              "sortBy": "top",
              # "sortBy": "popular",
              }
    print("requesting:", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:  # aiohttpp has "status"
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    # the url to the article itself is in data['articles'][i]['url']
    titles = [str(art['title']) + str(art['description'])
              for art in data['articles']]
    return titles


def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

def worker(*args):
    articles = get_articles(*args)
    q.put((len(articles), count_word(WORD, articles)))

def run_program():
    start = time.time()
    sources = get_sources()
    for source_name in sources:
        thread = threading.Thread(target=worker, args=(source_name,))
        thread.start()

    results = [q.get() for i in range(len(sources))]
    number_of_articles = sum([i[0] for i in results])
    number_of_occurrences = sum([i[1] for i in results])
    end = time.time()

    print('Found {} {} times in {} articles'.format(WORD, number_of_occurrences,
          number_of_articles))
    print('Search took {} seconds'.format(end-start))
    
if __name__ == '__main__':
    run_program()