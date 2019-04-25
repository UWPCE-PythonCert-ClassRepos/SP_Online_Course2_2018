#!/usr/bin/env python3

import threading
import queue
import requests
import time

WORD = "Washington"
NEWS_API_KEY = "ecb21f8a092f4a2aa79f57f96c190055"

base_url = 'https://newsapi.org/v1/'


def get_sources():
    url = base_url + "sources"
    params = {"language": "en",
              "apiKey": NEWS_API_KEY}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the sources")
    print(sources)
    return sources


def get_articles(source):
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"}

    print("Requesting: ", source)
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("Something went wrong with {}".format(source))
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


if __name__ == '__main__':
    start = time.time()
    news_queue = queue.Queue()

    def add_news_queue(*args):
        news_queue.put(get_articles(*args))

    sources = get_sources()
    threads = []

    for s in sources:
        thread = threading.Thread(target=add_news_queue, args=(s,))
        thread.start()
        print("Thread %s started" % thread.name)
        threads.append(thread)

    for t in threads:
        t.join()

    word_count = count_word(WORD, sources)
    art_count = len(sources)

    print(f'Found {WORD}, {word_count} times in {art_count} articles')
    print(f'Process took {(time.time() - start):.0f} sec.')