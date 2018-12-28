"""
Lesson 9 Assignment - Second Attempt

Making a multi-threaded version of the newsapi downloader

Takes advantage of:

uses data from the NewsAPI:

https//newsapi.org

"""

import time
import threading
import requests
import queue


WORD = "California"

NEWS_API_KEY = "dfed4429bb0a49bca151c9f7432f35c4"

base_url = 'https://newsapi.org/v1/'


# Same as single threading example from lecture video
def get_sources():
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the sources")
    print(sources)
    return sources


# Same as single threading example from lecture video
def get_articles(source):
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top",}
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


# Same as single threading example from lecture video

def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


# From here, code is refactored based on office hours help

sources = get_sources()
queues = queue.Queue()


# Add to queue
def put_queue(sources): 
    queues.put(get_articles(sources))


# counting words in the article in the queue
def count_words_in_the_articles_in_the_queues(queues):
    global word_count
    while not queues.empty():
        list_of_articles = queues.get()
        for article in list_of_articles:
            if WORD in article:
                word_count += 1


def multi_threading():
    threads = []

    for source in sources[:5]:
        thread = threading.Thread(target=put_queue, args=(source,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        print("joining thread:", thread.name)
        thread.join()
    print("all threads finished")


if __name__ == "__main__":

    start = time.time()

    word_count = 0

    put_queue(sources) # Into the queue

    multi_threading()

    count_words_in_the_articles_in_the_queues(queues) # out of queue

    print(WORD, "found {} times". format(word_count))
    print("Process took {:.0f} seconds".format(time.time() - start))










"""
import time
import threading
import requests
#import Queue


WORD = "iPhone"

NEWS_API_KEY = "dfed4429bb0a49bca151c9f7432f35c4"

base_url = 'https://newsapi.org/v1/'


# Same as single threading example from lecture video
def get_sources():
    url = base_url + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("all the sources")
    print(sources)
    return sources


# Same as single threading example from lecture video
def get_articles(source):
    url = base_url + "articles"
    params = {"source": source,
              "apiKey": NEWS_API_KEY,
              "sortBy": "top",}
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


# Same as single threading example from lecture video

def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


# Need to change scipt to change from single to multi ...

def multi_threading():

    start = time.time()
    sources = get_sources()
    art_count = 0
    word_count = 0

    threads = []

    for source in sources:
        thread = threading.Thread(target=get_articles(source), args=(source, titles,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        art_count += len(titles)
        word_count += count_word('iPhone', titles)
        print("joining thread:", thread.name)
        thread.join()
    print("all threads finished")

    '''
    # single threading example:
    for source in sources:
        titles = get_articles(source)
        art_count += len(titles)
        word_count += count_word('iPhone', titles)
    '''

    print(WORD, "found {} times in {} articles". format(word_count, art_count))
    print("Process took {:.0f} seconds".format(time.time() - start))

if __name__ == "__main__":
    multi_threading()
"""



