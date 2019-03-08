#!/usr/bin/env python

import time
import requests
import threading
import queue

WORD = "trump"

NEWS_API_KEY ='67c69a5ddb0e4951aa5b72d2ac100d6f'
#'67c69a5ddb0e4951aa5b72d2ac100d6f'
base_url = 'https://newsapi.org/v1/'


def get_sources():
    """
    Get all the english language sources of news
    """
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("List of source sites:\n")
    print(sources)
    return sources


def get_articles(source):
    """
    Get all the articles from sources
    """
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top",
              }
    print("requesting:", source)
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
    """count occurences of word in titles, returns the count"""
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

def search(*args):
    titles = get_articles(source)
    return(count_word(WORD, titles),len(titles))

def worker(*args):
    results.put(search(*args))

if __name__ == "__main__":
    results = queue.Queue()
    start_time = time.time()
    sources = get_sources()#[:5]
    threads=[]
    for source in sources:
        thread = threading.Thread(target=worker, args=(source,results,))
        threads.append(thread)
        thread.start()
        print("Thread %s started" % thread.name)
    for thread in threads:
        thread.join()

    occurrences = 0
    articles = 0
    while not results.empty():
        matches = results.get()
        occurrences += matches[0]
        articles += matches[1]
    print('\n---------------------------------------')
    print("Word: {} found {} times in {} articles".format(WORD, occurrences, articles))
    print("Process took {:.0f} seconds".format(time.time() - start_time))
