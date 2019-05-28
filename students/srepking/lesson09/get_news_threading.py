#!/usr/bin/env python

"""
Lesson 9 NewsAPI with threading.

Uses data from the NewsAPI:

https://newsapi.org
"""
import requests
import json
import time
import threading
import queue
import logging
from multiprocessing.pool import ThreadPool
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#NEWS_API_KEY = "d10950f416a940afa5f7f7ef103207d9"  # Shane's key
NEWS_API_KEY = "84d0483394c44f288965d7b366e54a74"

WORD = "war"
base_url = 'https://newsapi.org/v1/'


def get_sources():
    """
    Get all the english language sources of news

    'https://newsapi.org/v1/sources?language=en'
    Once we have the list of sources, we will make a request for each source
    to search for the word. This code does not need multiple threads, as it
    is a single request.
    """
    source_list = []
    url = base_url + "sources"
    params = {"language": "en", "apiKey": NEWS_API_KEY}
    resp = requests.get(url, params=params)
    data = resp.json()
    source_list.extend([src['id'].strip() for src in data['sources']])
    print("Got the sources")
    logger.debug('Print the sources from logger:')
    for source_item in source_list:
        logger.debug(source_item)
    return source_list


def get_articles(source):
    """
    For each source from 'get_sources', this method requests the title and
    article description and puts the string into a list called 'titles'. This
    title list will be later searched for our 'WORD'. Because we have multiple
    sources, we will want to be able to make this request concurrently,
    possibly one request for each source, but not nesessarily.

    Each thread passes in a list of sources until all lists are exhausted
    from the queue.
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

    titles.extend([(str(art['title']) + str(art['description']))
                   for art in data['articles']])



def count_word(word, titles):
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


if __name__ == '__main__':
    start = time.time()
    num_threads = 10
    API_sources = get_sources()
    titles = []
    # We do not want a request for each source, so we find a way to lump a
    # a bunch or requests into a queue. We will create the number in the queue
    # based on the number of threads we want to create.
    #list_length = int(len(API_sources)/num_threads)
    # Create a Pool to run all the threads in the queue
    q = queue.Queue() #this queue will hold a set of sources


    # Putting all of the sources to the queue.
    for source in API_sources:
        q.put(source)

    pool = ThreadPool(num_threads) # start threads

    while q.empty() is False:
        try:
            item = q.get()  # item is a source from the queue. This
            # source gets passed into the threadpool.
            logger.debug('Working on Source:')
            logger.debug(item)
            pool.apply_async(get_articles, args=(item,))
        except queue.Empty:
            break
    logger.debug('Made it out of while loop')
    pool.close()
    pool.join()
    # Count the number of titles that had WORD in it.
    art_count = len(titles)
    word_count = count_word(WORD, titles)

    print(f'found {WORD}, {word_count} times in {art_count} articles')
    print(f'Process took {(time.time() - start):.0f} sec.')


#    get_articles('abc-news-au')
#    logger.debug('Print titles after get_articles')
#    logger.debug(titles)
