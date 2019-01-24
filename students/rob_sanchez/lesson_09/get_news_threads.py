#!/usr/bin/env python

"""
The regular synchronous script has been revised to run using threads to count
the number of times a given word is mentioned in the top news articles of the day.

The synchronous script took about 27 seconds to run.

This threaded version took about 1 second to run.

Uses data from the NewsAPI:

https://newsapi.org

NOTE: you need to register with the web site to get a KEY.
"""
import time
import requests
import threading
import queue

WORD = "trump"

NEWS_API_KEY = "572ce06373144c978aa06bddcd27b07a"

base_url = 'https://newsapi.org/v1/'

# A new queue for the news articles
art_queue = queue.Queue()


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
    """
        Returns the number of times a word is found in
        the given article.
    """
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


def threading_integrate(*args):
    """
        Adds all articles found to the queue
    """

    art_queue.put(get_articles(*args))


if __name__ == "__main__":

    article_count = 0
    word_count = 0

    start = time.time()
    sources = get_sources()

    threads = []

    for source in sources:
        thread = threading.Thread(target=threading_integrate, args=(source,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    for i in sources:
        titles = art_queue.get()
        article_count += len(titles)
        word_count += count_word(WORD, titles)

    print("\'{}\' found {} times in {} articles".format(WORD, word_count, article_count))
    print("Process took {:.0f} seconds".format(time.time() - start))
