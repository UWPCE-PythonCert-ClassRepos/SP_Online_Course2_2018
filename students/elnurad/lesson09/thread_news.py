#!/usr/bin/env python

"""
Multithreading version of news api
"""

import time
import requests
import threading
import queue

WORD = "trump"

NEWS_API_KEY = "a70a2a99a1834ae8a2a738a5a56f24c2"

base_url = 'https://newsapi.org/v1/'
q = queue.Queue()


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
    return sources #got the list of resources


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
    q.put(titles)
    return titles


def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


start = time.time()
sources = get_sources()
threads = []
for source in sources:
    t = threading.Thread(target = get_articles, name = 'thread{}'.format(source), args = (source,))
    t.start()
    print('requesting {} complete'.format(t.name))
    threads.append(t)        
for t in threads:
    t.join()
art_count = 0
word_count = 0
num = len(sources)
for i in range(num):
    titles = q.get()
    art_count+= len(titles)
word_count += count_word('trump', titles)
print(WORD, "found {} times in {} articles".format(word_count, art_count))
print("Process took {:.0f} seconds".format(time.time() - start))

