#!/usr/bin/env python3

import configparser
import requests
import threading
from pathlib import Path
import time
import queue

config_file = Path(__file__).parent / '.config/config.ini'
config = configparser.ConfigParser()

try:
    config.read(config_file)
    key = config["scraper"]["key"]

except Exception as e:
    print(f'error: {e}')

base_url = 'https://newsapi.org/v1/'

word = 'trump'

results = queue.Queue()

def get_sources():
    """
    Get all the English language sources of news

    'https://newsapi.org/v1/sources?language=en'
    """
    url = base_url + "sources"
    params = {'language': 'en'}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("All the Sources")
    return sources


def get_articles(source):
    """
    https://newsapi.org/v1/articles? + parameters
    """
    url = base_url + "articles"
    params = {'source': source,
              'apiKey': key,
              'sortBy': "top"
              }
    print("requesting: {}".format(source))
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return[]
    data = resp.json()
    titles = [str(art['title']) + str(art['description'])
              for art in data['articles']]
    results.put(titles)
    return titles


def count_word(word, titles):
    word_to_find = word.lower()
    count = 0
    for title in titles:
        if word_to_find in title.lower():
            count += 1
    return count


if __name__ == '__main__':
    sources = get_sources()
    num_sources = len(sources)
    art_count = 0
    word_count = 0
    threads = []
    start = time.time()
    for source in sources:
        thread = threading.Thread(target=get_articles, args=(source,))
        thread.start()
        threads.append(thread)
    for i in range(num_sources):
        articles = results.get()
        art_count += len(articles)
        word_count += count_word(word, articles)
    print("Found \'{}\' {} times in {} articles".format(word, word_count, art_count))
    print("Process took {:.0f} seconds".format(time.time() - start))
