#!/usr/bin/env/python3
"""
A threaded news downloader to see how often a word was in the news headlines
"""

import requests
import threading
import queue
import time

sources = queue.Queue()
art_count = []
word_count = []


def get_sources(base_url):
    """
    Get all the english sources of news from the news api
    'https://newsapi.org/v1/sources?language=en'
    """
    global sources

    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    for src in data['sources']:
        sources.put(src['id'].strip())


def get_articles(source, base_url, NEWS_API_KEY):
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top"}
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    titles = [str(art['title']) + str(art['description']) for art in data['articles']]
    return titles


def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


def get_frequency(word, base_url):
    NEWS_API_KEY = ''

    global tasks, word_count, article_count

    while True:
        source = sources.get()
        if source is None:
            break
        print(source)
        titles = get_articles(source, base_url, NEWS_API_KEY)
        word_count.append(count_word(word, titles))
        art_count.append(len(titles))
        sources.task_done()


def news_frequency(word, num_threads=1):
    base_url = 'https://newsapi.org/v1/'
    start = time.time()

    global sources, word_count, art_count

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=get_frequency, args=(word, base_url))
        thread.start()
        threads.append(thread)

    get_sources(base_url)

    sources.join()
    for i in range(num_threads):
        sources.put(None)
    for thread in threads:
        thread.join()

    print(word, "found {} times in {} articles.".format(sum(word_count), sum(art_count)))
    print("Process took {:0f} seconds".format(time.time() - start))

    return word_count, art_count


if __name__ == '__main__':
    news_frequency('trump', 10)
