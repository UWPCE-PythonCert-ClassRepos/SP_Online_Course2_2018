#!/usr/bin/env python3

import logging
import requests
from threading import Thread
from queue import Queue

WORD = 'trump'
NEWS_API_KEY = "a41cdd2792c04abbab699e97662b5c0c"
BASE_URL = 'https://newsapi.org/v1/'

article_queue = Queue()
sources = []
titles = []


def get_sources(sources):
    """
    Ask newsapi.org for all news it has access to
    """
    url = BASE_URL + 'sources'
    params = {'language': 'en'}
    r = requests.get(url, params=params)
    data = r.json()
    sources.extend([src['id'].strip() for src in data['sources']])
    #  print sources
    return sources


def get_articles(source):
    print("Gathering Articles")
    url = BASE_URL + 'articles'
    params = {
        'source': source,
        'apiKey': NEWS_API_KEY,
        'sortBy': 'top'
        }
    print('Requesting: ', source)
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print('Error with {}'.format(source))
        return
    data = r.json()
    print('Got all articles from {}'.format(source))
    titles = [str(art['title']) + str(art['description']) for art in data['articles']]
    article_queue.put(titles)
    return titles


def count(word, titles):
    search_word = word.lower()
    count = 0
    for t in titles:
        if search_word in t.lower():
            count += 1
    return count


if __name__ == '__main__':
    get_sources(sources)

    source_list = []
    sources = sources[:5]

    for source in sources:
        t = Thread(target=get_articles, args=(source,))
        t.start()
        source_list.append(t)

    for thread in source_list:
        thread.join()

    sources_len = len(sources)
    word_count = 0
    for i in range(sources_len):
        a = article_queue.get()
        word_count += count(WORD, a)

print('"{}" was found {} times'.format(WORD, word_count))
