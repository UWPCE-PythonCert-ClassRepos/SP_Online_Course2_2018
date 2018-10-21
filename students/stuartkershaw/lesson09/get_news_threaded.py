#!/usr/bin/env python

"""
A Threaded version of the script to see how much a given word is
mentioned in the news today

Uses data from the NewsAPI:

https://newsapi.org
"""

import time
import requests
import threading

from queue import Queue
from multiprocessing.pool import ThreadPool

NEWS_API_KEY = "db0200d972284abc99e39877ad49cee5"

WORD = "Kavanaugh"
base_url = 'https://newsapi.org/v1/'


def get_sources():
    """
    https://newsapi.org/v1/sources?language=en
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
              "sortBy": "top",
              }
    print("requesting {} from {}.".format(source, threading.current_thread().name))
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
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


def producer(queue):
    while True:
        source = queue.get()

        if source is None:
            break

        consumer(get_articles(source))

        queue.task_done()


def consumer(titles):
    articles_count = len(titles)
    words_count = count_word(WORD, titles)

    global word_total
    word_total += words_count

    global art_total
    art_total += articles_count


start = time.time()
sources = get_sources()

thread_count = 10
jobs_queue = Queue(maxsize=10)

word_total = 0
art_total = 0

threads = []
for i in range(thread_count):
    thread = threading.Thread(target=producer, args=(jobs_queue,))
    thread.start()
    threads.append(thread)

for source in sources:
    jobs_queue.put(source)

jobs_queue.join()

for i in range(thread_count):
    jobs_queue.put(None)

for thread in threads:
    thread.join()

print("Threads finished.")

print(WORD, "found {} times in {} articles".format(word_total, art_total))
print("Process took {:.0f} seconds".format(time.time() - start))
