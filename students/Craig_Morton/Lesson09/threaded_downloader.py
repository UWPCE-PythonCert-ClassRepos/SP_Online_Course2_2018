# ------------------------------------------------- #
# Title: Lesson 9, Threaded Downloader
# Dev:   Craig Morton
# Date:  1/1/2019
# Change Log: CraigM, 1/2/2019, Threaded Downloader
# ------------------------------------------------- #

""" Use of threading for news gathering. """

import time
import threading
import requests
from queue import Queue

WORD = "technology"
NEWS_API_KEY = "5d237a99c69842c58b9a90b28d9d9581"
base_url = 'https://newsapi.org/v1/'

search = Queue()
search = Queue(maxsize=10)
search = Queue(maxsize=20)


def source_retrieve():
    """Get all the english language sources of news 'https://newsapi.org/v1/sources?language=en'"""
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("List of source sites:\n")
    print(sources)
    return sources


def articles_retrieve(source):
    """https://newsapi.org/v1/articles?source=associated-press&sortBy=top&apiKey=1fabc23bb9bc485ca59b3966cbd6ea26"""
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


def word_count(word, titles):
    """Word counter"""
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


def helper(*args):
    articles = articles_retrieve(*args)
    search.put((len(articles), word_count(WORD, articles)))


def program_execute():
    """Execute threaded downloader"""
    start = time.time()
    sources = source_retrieve()
    for source_name in sources:
        thread = threading.Thread(target=helper, args=(source_name,))
        thread.start()
    results = [search.get() for i in range(len(sources))]
    number_of_articles = sum([i[0] for i in results])
    number_of_occurrences = sum([i[1] for i in results])
    end = time.time()
    print('\nFound {} {} times in {} articles\n'.format(WORD, number_of_occurrences,
                                                        number_of_articles))
    print('This search took {} seconds'.format(end - start))


if __name__ == '__main__':
    program_execute()
