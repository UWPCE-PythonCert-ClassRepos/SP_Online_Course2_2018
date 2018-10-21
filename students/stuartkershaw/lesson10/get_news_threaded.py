#!/usr/bin/env python

"""
A Threaded version of the script to see how much a given word is
mentioned in the news today

Uses data from the NewsAPI:

https://newsapi.org
"""

import requests

from concurrent import futures

MAX_WORKERS = 10

NEWS_API_KEY = "db0200d972284abc99e39877ad49cee5"

WORD = "kavanaugh"

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


def process_titles(titles):
    articles_count = len(titles)
    words_count = count_word(WORD, titles)

    global word_total
    word_total += words_count

    global art_total
    art_total += articles_count


def get_titles(sources):
    workers = MAX_WORKERS

    with futures.ThreadPoolExecutor(workers) as executor:

        queue = []
        for source in sources:
            future = executor.submit(get_articles, source)
            queue.append(future)
            msg = "{}: {} was appended to the queue."
            print(msg.format(source, future))

        results = []
        for future in futures.as_completed(queue):
            res = future.result()
            msg = "{} results: {!r}"
            print(msg.format(future, res))
            results.append(res)

    return results


sources = get_sources()

word_total = 0
art_total = 0

titles = get_titles(sources)

for title in titles:
    process_titles(title)

print(WORD, "found {} times in {} articles".format(word_total, art_total))
