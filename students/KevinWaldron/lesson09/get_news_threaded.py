#!/usr/bin/env python

"""
An Asynchronous version of the script to see how much a given word is
mentioned in the news today

Uses data from the NewsAPI:

https://newsapi.org
"""

import time
import requests
from threading import Lock, Thread
from queue import Queue

NEWS_API_KEY = "0e3e584fc2f2487784c4dc07922b2f1c"

WORD = "Trump"
base_url = 'https://newsapi.org/v1/'

sources = Queue()

lock = Lock()

# This has to run first, so doesn't really need async
# but why use two requests libraries ?
def get_sources(sources):
    """
    Get all the english language sources of news

    'https://newsapi.org/v1/sources?language=en'
    """
    url = base_url + "sources"
    params = {"language": "en", "apiKey": NEWS_API_KEY}
    r = requests.get(url, params=params)

    if r.status_code != 200:  # check for valid status
        print(f'something went wrong: {r.status_code}')
        return

    data = r.json()
    print(f"Got the sources" )
    for src in data['sources']:
        sources.put(src['id'].strip())

def get_articles():
    while not sources.empty():
        """
        download the info for all the articles
        """
        source = sources.get()
        url = base_url + "articles"
        params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"
              }
        print("requesting:", params)
        r = requests.get(url, params=params)
        if r.status_code != 200:  # check for valid status
            print(f'something went wrong with: {source} code: {r.status_code}')
            sources.task_done()
            return

        print("got the articles from {}".format(source))
        data = r.json()
        # the url to the article itself is in data['articles'][i]['url']
        lock.acquire()
        titles.extend([(str(art['title']) + str(art['description']))
                   for art in data['articles']])
        lock.release()
        sources.task_done()


def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

if __name__ == '__main__':
    start = time.time()

    titles = []

    # get the sources -- this is synchronous
    get_sources(sources)

    threads = []
    for i in range(60):
        thread = Thread(target=get_articles)
        threads.append(thread)
        thread.start()

    sources.join()

    art_count = len(titles)
    word_count = count_word(WORD, titles)

    print(f'found {WORD}, {word_count} times in {art_count} articles')
    print(f'Process took {(time.time() - start):.0f} sec.')
