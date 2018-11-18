#!/usr/bin/env python3
"""
Lesson 09
In this lesson, we looked at an asyncio based web data scraper.
In that case, there were about 100 simultaneous requests. Async is very well suited to many requests, but for 100 or so, 
a multi-threaded approach could work well too. So your job is to make a multi-threaded version of the newsapi downloader:
Complete description here: A Threaded Downloader (Links to an external site.)Links to an external site.
"""

import logging
import threading
import queue
import requests
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = 'https://newsapi.org/v1/'
SEARCH_WORD = 'fire'
API_KEY = '41e5de7149fc41c1a2889cd712e3acb6'

ARTICLECOUNT = 0
WORDCOUNT = 0

def get_sources():
    """Gets sources from the API"""
    logger.info('Getting List of New Sources')
    url = f'{BASE_URL}sources'
    params = {'language': 'en'}
    response = requests.get(url, params=params)
    data = response.json()
    srcs = [src['id'].strip() for src in data['sources']]

    logger.info(f'List of News Sources:{srcs}')

    return srcs


def get_articles(source):
    """pulls lists of articles from source from API"""

    logger.info(f'Getting articles for: {source}')
    url = f'{BASE_URL}articles'
    params = {'source': source,
              'apiKey': API_KEY,
#              'sortBy': 'latest', #some sources don't support latest
              'sortBy': 'top',
#              'sortBy': 'popular',
              }
    logger.info(f'Requesting {source}')
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        logger.info(f'An issue happened with {source}')
        logger.info(resp)
        logger.info(resp.text)

        return []
    data = resp.json()
    #the url to the article itself is in data['articles'][i]['url']
    titles = [str(art['title']) + str(art['description'])
              for art in data['articles']]
    return titles


def get_word_count(word, titles):
    """Gets the word count of the search word in the article/titles """

    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count


def threading_processing():
    """This is the threading function. Also populates the article and wordcount"""
    try:
        source = sources.pop()
    except IndexError:
        pass
    articles = get_articles(source)

    #Getting Word and Article Count
    global WORDCOUNT
    WORDCOUNT += get_word_count(SEARCH_WORD, articles)
    global ARTICLECOUNT
    ARTICLECOUNT += len(articles)

""" Main code """
threads = []
start_time = time.time()
sources = get_sources()

logger.info('Getting Article and wordcount')
for s in range(len(sources)):
    thread = threading.Thread(target=threading_processing, args=())
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

#Output - prints articles searched and count of word
print(f'{ARTICLECOUNT} articles searched. The word: {SEARCH_WORD} appeared {WORDCOUNT} times ')
#For fun grabbing the time the process took.
end_time = time.time() - start_time
print(f'This process ran in {end_time:.02f} seconds')
