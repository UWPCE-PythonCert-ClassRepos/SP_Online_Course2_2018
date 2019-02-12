#!/usr/bin/env python

"""
An Asynchronous version of the script to see how much a given word is
mentioned in the news today

Uses data from the NewsAPI:

https://newsapi.org
"""

import time
import requests
import threading
from queue import Queue

NEWS_API_KEY = "84d0483394c44f288965d7b366e54a74"

WORD = "war"
base_url = 'https://newsapi.org/v1/'


def get_sources(sources):
    """
    Get all the english language sources of news

    'https://newsapi.org/v1/sources?language=en'
    """
    url = base_url + "sources"
    params = {"language": "en", "apiKey": NEWS_API_KEY}
    r = requests.get(url, params=params)
    data = r.json()
    print("Got the sources")
    sources.extend([src['id'].strip() for src in data['sources']])
    r.close()


def get_articles(source):
    """
    download the info for all the articles
    """
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"
              }
    print("requesting:", source)
    r = requests.get(url, params=params)
    print("got the articles from {}".format(source))
    data = r.json()
    lock.acquire()
    # the url to the article itself is in data['articles'][i]['url']
    titles.extend([(str(art['title']) + str(art['description']))
                   for art in data['articles']])
    lock.release()
    r.close()


def worker():
    while True:
        item = q.get()
        if item is None:
            break
        get_articles(item)
        q.task_done()


def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


start = time.time()

# create the objects to hold the data
sources = []
titles = []

# get the sources
get_sources(sources)

# setup queue with all the sources
q = Queue()
for source in sources:
    q.put(source)

# run threads through the sources in queue
threads = []
max_threads = 40
#             20 tock 2.4 seconds
#             50 took 1.6 seconds
#             75 took 1.6 second
#
lock = threading.Lock()
for i in range(max_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)


q.join() # blocking until all tasks in queue are complete
art_count = len(titles)
word_count = count_word(WORD, titles)

print(f'found {WORD}, {word_count} times in {art_count} articles')
print(f'Process took {(time.time() - start):.1f} sec.')

# stop workers
for i in range(max_threads):
    q.put(None)
for t in threads:
    t.join()