#!/usr/bin/env python
# Lesson 9, threaded news web scraper

import time
import requests
from threading import Lock, Thread
from queue import Queue

NEWS_API_KEY = "b28ceb3c16c445e197b8b18f79c35821"
BASE_URL = 'https://newsapi.org/v1/'
WORD = "Trump"

sources = Queue()

lock = Lock()

def get_sources(sources):
    """
    Get all the sources of news (English only)
    """
    url = BASE_URL + "sources"
    params = {"language": "en", "apiKey": NEWS_API_KEY}
    r = requests.get(url, params=params)

    if r.status_code != 200:  # valid status
        print("ERROR: ", r.status_code)
        return

    data = r.json()
    print("Getting sources..." )
    for src in data['sources']:
        sources.put(src['id'].strip())

def get_articles():
    while not sources.empty():
        """
        Get info for all articles
        """
        source = sources.get()
        url = BASE_URL + "articles"
        params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"
              }
        print("Requesting: ", params)
        r = requests.get(url, params=params)
        if r.status_code != 200:  # valid status?
            print("ERROR - source: {} with code: {}".format(source, r.status_code))
            sources.task_done()
            return

        print("Retrieved articles from source {}".format(source))
        data = r.json()
        lock.acquire()
        titles.extend([(str(art['title']) + str(art['description']))
                   for art in data['articles']])
        lock.release()
        sources.task_done()


def count_words(word, titles):
    """
    Count instances of the given word in the given titles
    """
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

if __name__ == '__main__':
    start = time.time()

    titles = []

    get_sources(sources)

    threads = []
    for i in range(60):
        thread = Thread(target=get_articles)
        threads.append(thread)
        thread.start()

    sources.join()

    num_articles = len(titles)
    word_count = count_words(WORD, titles)

    print("Counted {} instances of the word {} in {} articles".format(word_count, WORD, num_articles))
    print("This processing took took {:.2f} seconds".format((time.time() - start)))
