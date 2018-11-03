#!/usr/bin/env python

"""
Threaded version of the script to see how much a given word is
mentioned in the news today

Uses data from the NewsAPI:

https://newsapi.org
"""

import threading
import requests

from queue import Queue

NEWS_API_KEY = "5e3dca56fa674afe9b01464c3bd308e8"

WORD = "war"
base_url = 'https://newsapi.org/v1/'


def get_sources():
    """
    Get all the english language sources of news

    'https://newsapi.org/v1/sources?language=en'
    """
    url = base_url + "sources"
    params = {"language": "en", "apiKey": NEWS_API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("Got the sources:")
    print(sources)
    return sources


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
    response = requests.get(url, params=params)
    if response.status_code != 200:  # requests has "status"
        print(f'something went wrong with: {source}')
        print(response)
        print(response.text)
        return []
    data = response.json()
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


if __name__ == "__main__":
    news_queue = Queue()

    def add_news_queue(*args):
        news_queue.put(get_articles(*args))

    # create the objects to hold the data
    sources = get_sources()
    threads = []

    for item in sources:
        thread = threading.Thread(target=add_news_queue, args=(item,))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
